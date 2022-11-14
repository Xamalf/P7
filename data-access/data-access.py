from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI(root_path="/data-access")

uvicorn.run(app, host="0.0.0.0", port=5000)