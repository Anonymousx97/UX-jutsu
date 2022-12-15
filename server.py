from fastapi import FastAPI
import uvicorn
import asyncio


app = FastAPI()

@app.get("/")
async def read_root():
    return "healthy"

if __name__=="__main__":
    uvicorn.run(app,workers=1,host ="0.0.0.0" ,port=10000)
