from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI(title="Alignzo API Gateway (BFF)")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service URLs
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:8000")
ORCHESTRATOR_URL = os.getenv("ORCHESTRATOR_URL", "http://orchestrator:8000")
PROJECT_SERVICE_URL = os.getenv("PROJECT_SERVICE_URL", "http://project-service:8000")
LOGGING_SERVICE_URL = os.getenv("LOGGING_SERVICE_URL", "http://logging-service:8000")

@app.get("/health")
def health():
    return {"status": "ok", "service": "api-gateway"}

@app.get("/services/health")
async def services_health():
    """Check health of all services"""
    services = {
        "user-service": USER_SERVICE_URL,
        "orchestrator": ORCHESTRATOR_URL,
        "project-service": PROJECT_SERVICE_URL,
        "logging-service": LOGGING_SERVICE_URL
    }
    
    health_status = {}
    async with httpx.AsyncClient() as client:
        for service_name, service_url in services.items():
            try:
                response = await client.get(f"{service_url}/health", timeout=5.0)
                health_status[service_name] = {
                    "status": "healthy" if response.status_code == 200 else "unhealthy",
                    "status_code": response.status_code
                }
            except Exception as e:
                health_status[service_name] = {
                    "status": "unhealthy",
                    "error": str(e)
                }
    
    return health_status

# User Service Routes
@app.get("/users/{path:path}")
async def user_service_proxy(path: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{USER_SERVICE_URL}/users/{path}")
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.post("/users/{path:path}")
async def user_service_proxy_post(path: str, request: dict):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{USER_SERVICE_URL}/users/{path}", json=request)
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# Orchestrator Routes
@app.get("/orchestrator/{path:path}")
async def orchestrator_proxy(path: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{ORCHESTRATOR_URL}/{path}")
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# Project Service Routes
@app.get("/projects/{path:path}")
async def project_service_proxy(path: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{PROJECT_SERVICE_URL}/projects/{path}")
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.post("/projects/{path:path}")
async def project_service_proxy_post(path: str, request: dict):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{PROJECT_SERVICE_URL}/projects/{path}", json=request)
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) 