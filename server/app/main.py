from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router

app = FastAPI(title="Social Graph API")

# CORS configuration - development convenience
# WARNING: allow_origins=["*"] permits any origin. Use only for local/dev testing.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # DEV ONLY: allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
