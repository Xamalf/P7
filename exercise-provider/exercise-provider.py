from fastapi import FastAPI, HTTPException, Cookie, Response
import requests
import uvicorn
from pydantic import BaseModel
import glob
import re

app = FastAPI(root_path="/exercise-provider")

class Exercise_id(BaseModel):
    id: int

class Token(BaseModel):
    access_token: str
    refresh_token: str


def userAuth(token: Token):
    auth_response = requests.post("http://auth.default:3000/auth/username",
                                  json={"access_token": token.access_token, "refresh_token": token.refresh_token})

    if auth_response.status_code != 200:
        raise HTTPException(
            status_code=404,
            detail="Auth failed"
        )

    return auth_response.json()


# @app.post("/exercise-provider")
# async def root(exercise_id: Exercise_id):
#     try:
#         auth_response = requests.post("http://auth.default:3000/auth", json={"name": "tester"}) # Calling auth
#         # exercise_response = await data_base # Calling exercise database
#         if auth_response.status_code != 200:
#             raise HTTPException(
#                 status_code=404,
#                 detail="Auth failed"
#             )
#     except Exception:
#         raise HTTPException(
#             status_code=404,
#             detail="Auth failed"
#         )
#
#     with open("exercises/2.xml", "rb") as f:
#         text = f.read()
#
#     return Response(content=text, media_type="application/xml")

@app.post("/exercise-provider/verify")
async def root(exercise_id: Exercise_id):

    with open(f"exercises/{exercise_id.id}.xml", "rb") as f:
        text = f.read().decode('utf-8')

    jsonObject = {}

    match = re.search(r"([\s\S]*)<template>[\s\S]*</template>([\s\S]*)", text)

    jsonObject.update({
        "beginning": match.group(1),
        "end": match.group(2)
    })

    return jsonObject

@app.post("/exercise-provider/client")
async def root(exercise_id: Exercise_id, access_token: str = Cookie(None), refresh_token: str = Cookie(None)):
    try:
        auth_response = userAuth(Token(access_token=access_token, refresh_token=refresh_token)) # Calling auth
    except Exception:
        raise HTTPException(
            status_code=404,
            detail="Auth failed"
        )

    with open(f"exercises/{exercise_id.id}.xml", "rb") as f:
        text = f.read().decode('utf-8')

    match = re.search(r"(<template>[\s\S]*</template>)", text)

    jsonObject = {}

    jsonObject.update({
        "template" : match.group(1)
    })

    return jsonObject

@app.post("/exercise-provider/avalable-exercises")
async def root(access_token: str = Cookie(None), refresh_token: str = Cookie(None)):
    try:
        auth_response = userAuth(Token(access_token=access_token, refresh_token=refresh_token))  # Calling auth
        # exercise_response = await data_base # Calling exercise database
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Auth failed + {e}"
        )

    files = glob.glob("./exercises/*.xml")

    files = [filename[12:-4] for filename in files]

    return files

uvicorn.run(app, host="0.0.0.0", port=2000)
