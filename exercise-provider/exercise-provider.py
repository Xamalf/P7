from fastapi import FastAPI
import requests

app = FastAPI()

@app.post("/exercise-provider")
async def root():

    auth_response = await requests.post("127.0.0.1:3000") # Calling auth
    # exercise_response = await data_base # Calling exercise database
    return {"message": "Hello from exercise provider!"}
