from fastapi import FastAPI
from .routers import companies, users, ratings, appreciations

app = FastAPI(title="Alignzo User Service")

app.include_router(companies.router)
app.include_router(users.router)
app.include_router(ratings.router)
app.include_router(appreciations.router)

@app.get("/health")
def health():
    return {"status": "ok"} 