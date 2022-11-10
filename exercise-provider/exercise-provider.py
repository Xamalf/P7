from fastapi import FastAPI, HTTPException
import requests
import uvicorn

app = FastAPI(root_path="/exercise-provider")

@app.post("/exercise-provider")
async def root():
    try:
        auth_response = requests.post("http://auth.default:3000/auth", {"name": "tester"}) # Calling auth
        # exercise_response = await data_base # Calling exercise database
        if auth_response.status_code != 200:
            raise HTTPException(
                status_code=404,
                detail="Auth failed"
            )
    except Exception:
        raise HTTPException(
            status_code=404,
            detail="Auth failed"
        )
    return {"message": f"Hello {auth_response.name} from exercise provider!"}

uvicorn.run(app, host="0.0.0.0", port=2000)
