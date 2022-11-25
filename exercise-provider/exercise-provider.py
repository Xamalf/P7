from fastapi import FastAPI, HTTPException, Response
import requests
import uvicorn
from pydantic import BaseModel

app = FastAPI(root_path="/exercise-provider")

class Exercise_id(BaseModel):
    id: int

@app.post("/exercise-provider")
async def root(exercise_id: Exercise_id):
    try:
        auth_response = requests.post("http://auth.default:3000/auth", json={"name": "tester"}) # Calling auth
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

    with open("exercises/2.xml", "rb") as f:
        text = f.read()

    return Response(content=text, media_type="application/xml")
    # return {"message": f"Hello {auth_response.json()['name']} from exercise provider!"}

uvicorn.run(app, host="0.0.0.0", port=2000)
