from fastapi import FastAPI
import uvicorn

app = FastAPI(root_path="/")

@app.get("/")
async def root():
    return {"message": "Hello from auth!"}


@app.post("/auth")
async def root():
    return {"message": "Hello from auth!"}

uvicorn.run(app, host="0.0.0.0", port=3000)