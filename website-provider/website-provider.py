from fastapi import FastAPI
import uvicorn

app = FastAPI(root_path="/website-provider")

@app.get("/website-provider")
async def root():
    return {"message": "Hello from website provider!"}

uvicorn.run(app, host="0.0.0.0", port=4000)
