from fastapi import FastAPI, HTTPException
import requests
import uvicorn

app = FastAPI(root_path="/exercise-verifier")

@app.post("/exercise-verifier")
async def root():
    try:
        auth_response = requests.post("http://auth:3000/auth") # Calling auth
        exercise_provider_response = requests.post("http://exercise-provider:2000/exercise-provider") # Calling exercise provider
        # user_dataresponse = await data_base # Calling user database
        if auth_response.status_code != 200 or exercise_provider_response.status_code != 200:
            raise HTTPException(
                status_code=404,
                detail="Auth or exercise_provider failed"
            )
    except Exception:
        raise HTTPException(
            status_code=404,
            detail="Auth or exercise_provider failed"
        )
    return {"message": "Hello from exercise verifier!"}

@app.get("/exercise-verifier")
async def root():
    try:
        auth_response = requests.post("http://localhost:3000/auth") # Calling auth
        exercise_provider_response = requests.post("http://localhost:2000/exercise-provider") # Calling exercise provider
        # user_dataresponse = await data_base # Calling user database
        if auth_response.status_code != 200 or exercise_provider_response.status_code != 200:
            raise HTTPException(
                status_code=404,
                detail="Auth or exercise_provider failed"
            )
    except Exception:
        raise HTTPException(
            status_code=404,
            detail="Auth or exercise_provider failed"
        )
    return {"message": "Hello from exercise verifier!"}

uvicorn.run(app, host="0.0.0.0", port=10000)
