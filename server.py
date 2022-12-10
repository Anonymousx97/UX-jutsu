from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return "working"

@app.get("/h")
async def read_h():
    return "healthy"
