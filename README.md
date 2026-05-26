# aekra-code-acp

ACP server that bridges VS Code (ACP client) to the **aekra-code-agent** LangGraph server.

The agent runs server-side and uses [aekra-core](../313326_aekra-core)'s
`InterruptSandbox` for every shell, file-read, file-edit, ls, glob, and grep
operation. Each operation suspends the run with a `sandbox.execute` interrupt;
this ACP server runs the command on the user's own machine via a local
`bash` subprocess and resumes the run with the result.

```
VS Code (ACP client)
   │  stdio / JSON-RPC
   ▼
aekra-code-acp  ──HTTP──▶ LangGraph server (aekra-code-agent)
   ▲                          │   InterruptSandbox.execute()
   │                          │   ↓ interrupt(sandbox.execute)
   │  ◀── interrupt ──────────┘
   │
   │  LocalExecutor: bash -c "<command>" in user's project cwd
   │
   └── resume run with {output, exit_code, truncated}
```

Execution is fully local — the agent never touches the user's
filesystem directly. No remote sandbox, no tunnels, no extra services
to run.

> **In a hurry?** Jump to [`QUICKSTART.md`](QUICKSTART.md) for a five
> minute walkthrough.

## Key features

- ACP agent (`AekraCodeACP`) that manages per-session state (cwd, assistant
  mode, model override, active run IDs, thread IDs).
- Mode and Model pickers surfaced to the VS Code client (Coding / Planning +
  model overrides).
- `LocalExecutor` runs every `sandbox.execute` interrupt locally. Cross
  platform: Git Bash on Windows, native bash on macOS / Linux. Auto-detects
  Python 3 and shims it as `python3` when required.
- Real-time streaming with message de-duplication and human-in-the-loop
  approval interrupts (Allow / Deny in VS Code) for write tools.

## Requirements

- Python 3.10+ on the user's machine.
- A LangGraph server running the `aekra-code-agent` graphs (`local-coding`
  and `local-planning`).
- **A shell**:
  - macOS / Linux: native `/bin/bash`. Pre-installed on every dev machine.
  - Windows: choose **either** Git Bash **or** WSL. Both are supported and
    selectable via `AEKRA_SHELL_KIND` (see below).
- **python3** must be reachable from the chosen shell.
  - Git Bash: needs Windows Python. The executor auto-detects `python3`,
    `python` (if it is Python 3), or `py -3`, and shims it as `python3`
    inside Git Bash. Override with `AEKRA_PYTHON`.
  - WSL: uses the distro's own `python3` (no shim). Make sure it's
    installed (`sudo apt install python3` on Ubuntu).
  - macOS / Linux: needs `python3` on PATH (almost always already there).

## Installation

```bash
pip install -e .
```

## Configuration (environment variables)

| Var | Default | Purpose |
| --- | --- | --- |
| `AEKRA_AGENT_URL` | `http://localhost:2025` | URL of the aekra-code-agent LangGraph server. |
| `AEKRA_DEFAULT_ASSISTANT` | `local-coding` | Assistant mode selected on new sessions (`local-coding` / `local-planning`). |
| `AEKRA_DEFAULT_MODEL` | `model:azure_openai:gpt-5-mini` | Default model mode ID. |
| `AEKRA_MODELS` | _(empty)_ | Comma-separated `model_id=DisplayName` pairs to populate the model picker. Example: `azure_openai:gpt-5-mini=GPT-5 Mini,anthropic:claude-sonnet-4-20250514=Claude Sonnet`. |
| `AEKRA_LOG_LEVEL` | `INFO` | Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`). |
| `AEKRA_SHELL_KIND` | `auto` | **Windows only.** `auto` (Git Bash preferred, WSL fallback), `gitbash`, or `wsl`. |
| `AEKRA_SHELL` | _(auto)_ | Override the shell binary. For `gitbash` set this to `bash.exe`; for `wsl` set it to `wsl.exe`. |
| `AEKRA_WSL_DISTRO` | _(default distro)_ | Optional WSL distro name passed to `wsl.exe -d <name>`. |
| `AEKRA_PYTHON` | _(auto)_ | Override the Python 3 interpreter that backs the Git Bash `python3()` shim. Ignored in WSL mode. |

## Wiring it up

1. Start the aekra-code-agent LangGraph server:

   ```bash
   cd 313326_aekra-code-agent
   aegra dev   # or however your local LangGraph server boots
   ```

2. Start the ACP server:

   ```bash
   aekra-code-acp
   ```

3. In VS Code, register the ACP server. The default assistant is
   `local-coding`, which uses `InterruptSandbox`. The Coding / Planning
   pickers map directly to `local-coding` / `local-planning` graphs in
   the agent.

## Cross-platform notes

### macOS / Linux

Paths flow through unchanged. The session `cwd` from VS Code becomes the
subprocess `cwd` and is also injected into the agent's prompt as
`working_directory`. Native `python3` is used.

### Windows + Git Bash (default)

```
AEKRA_SHELL_KIND=gitbash    # or just rely on the auto default
```

- Native Windows paths (`C:\Users\me\proj`) flow through unchanged. The
  agent sees them in its prompt and emits commands relative to that cwd.
- The deepagents `BaseSandbox` emits `python3 -c "..."` commands; the
  executor prepends a Bash `python3()` function shim that resolves to
  the host's Windows `python.exe`. Works with Python from the
  `python.org` installer, the Microsoft Store, or `py -3`.
- Heredocs (`<<'__DEEPAGENTS_EOF__'`) and `||` / `2>/dev/null` work
  natively because Git Bash is real GNU bash.

### Windows + WSL

```
AEKRA_SHELL_KIND=wsl
AEKRA_WSL_DISTRO=Ubuntu     # optional, defaults to the user's default distro
```

- Commands run via `wsl.exe --cd /mnt/c/Users/me/proj -- bash -c "..."`
  inside the chosen distro.
- The session `cwd` (Windows form `C:\Users\me\proj`) is automatically
  translated to `/mnt/c/Users/me/proj` at the boundary and **also** sent
  to the agent as its `working_directory`, so the agent's prompt and any
  absolute paths it emits stay consistent with what the WSL shell sees.
- Uses the distro's own `python3` — install it once inside WSL
  (`sudo apt install python3` on Ubuntu).

### Auto mode

`AEKRA_SHELL_KIND=auto` (the default) tries Git Bash first and falls
back to WSL if no Git Bash install is found. If both are missing, the
ACP server fails fast at startup with a clear message.

## Project layout

- `src/aekra_code_acp/server.py` — `AekraCodeACP` ACP agent.
- `src/aekra_code_acp/executor/local_executor.py` — `LocalExecutor`.
- `src/aekra_code_acp/streaming/streaming.py` — `StreamingService` and
  interrupt routing.
- `src/aekra_code_acp/modes.py` — assistant / model mode definitions.
- `src/aekra_code_acp/__main__.py` — CLI entry point.

## License

MIT
