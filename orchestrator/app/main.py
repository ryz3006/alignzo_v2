from fastapi import FastAPI
from .routers import tests, suites, runs, results, artifacts

app = FastAPI(title="Alignzo Test Orchestrator")

app.include_router(tests.router)
app.include_router(suites.router)
app.include_router(runs.router)
app.include_router(results.router)
app.include_router(artifacts.router)

@app.get("/")
def read_root():
    return {"message": "Alignzo Test Orchestrator API is running."} 