// demo.ts
// Simple TypeScript demo file

export function greet(name: string): string {
  return `Hello, ${name}!`;
}

export async function delayedGreet(name: string, ms = 500): Promise<string> {
  return new Promise((resolve) => {
    setTimeout(() => resolve(greet(name)), ms);
  });
}

// If run directly with ts-node or after compilation, print a demo greeting
if (require.main === module) {
  (async () => {
    const msg = await delayedGreet('World', 300);
    console.log(msg);
  })();
}
