from fastapi import FastAPI
import uvicorn
from fastapi.staticfiles import StaticFiles

app = FastAPI(root_path="/")

app.mount("/", StaticFiles(directory="dist", html=True), name="frontend")

uvicorn.run(app, host="0.0.0.0", port=4000)
