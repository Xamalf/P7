from requests import request
from fastapi import FastAPI
import requests

app = FastAPI()

@app.post("/exercise-verifier")
async def root():
    auth_response = await requests.post("127.0.0.1:3000") # Calling auth
    # user_data_response = await data_base # Calling user database
    return {"message": "Hello from exercise verifier!"}
