from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/website-provider")
async def root():
    return {"message": "Hello from website provider!"}

uvicorn.run(app, host="0.0.0.0", port=4000)
