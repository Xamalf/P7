from fastapi import FastAPI, HTTPException
import requests
import uvicorn
from pydantic import BaseModel
import subprocess
from uuid import uuid4
from os import remove
import json


app = FastAPI(root_path="/exercise-verifier")

class Xml_wrapper(BaseModel):
    id: int
    xml: str 


@app.post("/exercise-verifier")
async def root(xml_in_json: Xml_wrapper):
    try:
        auth_response = requests.post("http://auth.default:3000/auth", json={"name": "tester"}) # Calling auth
        exercise_provider_response = requests.post("http://exercise-provider.default:2000/exercise-provider/verify",
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

    file_name = "./exercises/" + str(uuid4()) + ".xml"

    template = json.loads(xml_in_json.json())
    provided = json.loads(exercise_provider_response.content.decode('utf-8'))

    print("--------------")
    print(template)
    print(provided["beginning"])
    print("--------------")

    text = provided["beginning"] + template["xml"] + provided["end"]

    print(text)

    with open(file_name, "wb") as f:
        f.write(text.encode())

    print("after write")

    output = subprocess.check_output(["./verifyer/verifyta", file_name])

    print("after call")

    remove(file_name)

    if b'Formula is NOT satisfied' in output:
        return {"message": f"Hello {auth_response.json()['name']} from exercise verifier! \n "
                           f"One or more queries NOT satisfied \n OUTPUT: \n {output}"}
    else:

        return {"message": f"Hello {auth_response.json()['name']} from exercise verifier! \n "
                           f"All queries satisfied \n OUTPUT: \n {output}"}


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
