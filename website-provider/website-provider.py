from fastapi import FastAPI

app = FastAPI()

@app.get("/website-provider")
async def root():
    return {"message": "Hello from website provider!"}
