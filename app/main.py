from fastapi import FastAPI
from app.auth.router import router as auth_router
from app.tasks import models as tasks_models
from app.tasks.router import router as tasks_router
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware

from app.middleware.rate_limit import limiter
app = FastAPI(title="TaskFlow CRUD")

@app.get("/")
async def intro():
    return f"Hello World"
@app.get("/health")
async def health_check():
    return {"status":"ok"}

app.include_router(auth_router)
app.include_router(tasks_router)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],
    allow_methods=["*"],
    allow_headers=["*"],
)