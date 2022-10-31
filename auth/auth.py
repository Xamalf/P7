from fastapi import FastAPI

app = FastAPI()

@app.post("/auth")
async def root():
    return {"message": "Hello from auth!"}
