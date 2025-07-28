from fastapi import FastAPI
from .routers import logs
from .config import print_config

app = FastAPI(title="Alignzo Logging Service")

print_config()

app.include_router(logs.router)

@app.get("/health")
def health():
    return {"status": "ok"} 