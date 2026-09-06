from fastapi import FastAPI
from app.auth.router import router as auth_router
from app.tasks import models as tasks_models
app = FastAPI(title="TaskFlow CRUD")

@app.get("/")
async def intro():
    return f"Hello World"
@app.get("/health")
async def health_check():
    return {"status":"ok"}

app.include_router(auth_router)

