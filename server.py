from fastapi import FastAPI
import uvicorn
import asyncio

app = FastAPI()

@app.get("/")
async def read_root():
    return "working"

@app.get("/h")
async def read_h():
    return "healthy"

uvicorn.run(app,workers=1,host ="0.0.0.0" ,port=10000)
