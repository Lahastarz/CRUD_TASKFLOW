from fastapi import FastAPI
app = FastAPI(title="TaskFlow CRUD")

@app.get("/")
async def intro():
    return f"Hello World"
@app.get("/health")
async def health_check():
    return {"status":"ok"}