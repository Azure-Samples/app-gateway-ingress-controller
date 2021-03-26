import uvicorn
from fastapi import FastAPI, Depends, HTTPException

app = FastAPI()


@app.get("/")
async def index():
    return {"message": "hello world"}


if __name__ == "__main__":
    uvicorn.run("api:app", port=8080, reload=True)
