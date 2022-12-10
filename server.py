from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return "working"

@app.get("/h")
def read_h():
    return "healthy"
