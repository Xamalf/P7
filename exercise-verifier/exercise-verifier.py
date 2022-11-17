from fastapi import FastAPI, HTTPException
import requests
import uvicorn
from pydantic import BaseModel

app = FastAPI(root_path="/exercise-verifier")

class Xml_wrapper(BaseModel):
    id: int
    xml: str 


@app.post("/exercise-verifier")
async def root(xml_in_json: Xml_wrapper):
    try:
        auth_response = requests.post("http://auth.default:3000/auth", json={"name": "tester"}) # Calling auth
        exercise_provider_response = requests.post("http://exercise-provider.default:2000/exercise-provider", 
            json={"id":xml_in_json.id}) # Calling exercise provider
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
        
    xml = xml_in_json.xml
    with open('exercise.xml', 'w') as f:
        f.write(xml)

    return {"message": f"Hello {auth_response.json()['name']} from exercise verifier!"}

@app.get("/exercise-verifier")
async def root():
    try:
        auth_response = requests.post("http://auth.default:3000/auth", json={"name": "tester"}) # Calling auth
        exercise_provider_response = requests.post("http://exercise-provider.default:2000/exercise-provider") # Calling exercise provider
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
