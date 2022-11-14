from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

class User_info(BaseModel):
    name: str
    
app = FastAPI(root_path="/")

@app.get("/")
async def root():
    return {"message": "Hello from auth!"}


@app.post("/auth")
async def root(user_info: User_info):
    print(user_info)
    return user_info

uvicorn.run(app, host="0.0.0.0", port=3000)