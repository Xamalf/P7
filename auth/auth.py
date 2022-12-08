from fastapi import FastAPI, Cookie, Response, HTTPException
import psycopg2
from pydantic import BaseModel
import uvicorn
import requests
from uuid import uuid4
app = FastAPI()

class User_info(BaseModel):
    name: str

class Code(BaseModel):
    code: str

class Token(BaseModel):
    access_token: str
    refresh_token: str

db_connection = psycopg2.connect(
            database="user_data_db",
            user="user",
            password="passw0rd124",
            host="user-db.default",
            port=5432,
        )

db_cursor = db_connection.cursor()    
db_connection.autocommit = True


@app.post("/auth/login")
def root(username: User_info, response: Response):
    db_cursor.execute('''SELECT name, email FROM users WHERE name = %s;''', [username.name])

    result = db_cursor.fetchone()
    
    if not result:
        print("User NOT authenticated - login exited")
        return {"name" : "no user", }
    else:
        print("User authenticated - login exited")
        response.set_cookie(key="cookie", value=result[0])
        return { "name": result[0] }


@app.post("/auth")
def root(code: Code, response: Response):  
    print("User auth code entered")

    try:
        print("Try block entered")
        auth_response = requests.post("http://google-verifier.default:6000/google-verifier",
        json={ "code": code.code })

        print("Auth response generated")

        if auth_response.status_code != 200:
            raise HTTPException(
                status_code=404,
                detail="Auth failed by status code != 200"
            )
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Auth failed by raised exception + { str(e) }"
        )

    response_tokens = auth_response.json()
    response.set_cookie(key="access_token", value=response_tokens["access_token"])
    response.set_cookie(key="refresh_token", value=response_tokens["refresh_token"])

    return { "token_cookie": "Token cookies created"}

@app.post("/auth/username")
def root(token: Token):  
    print("User token recieved entered")

    try:
        userinfo = requests.post("http://google-verifier.default:6000/google-verifier/token-verifier",
        json=token)
        print("Outside if")
        if userinfo.status_code != 200:
            print("Entered if!")
            raise HTTPException(
                status_code=404,
                detail="Auth failed by status code != 200"
            )


    except Exception:
        print("Entered exception")
        raise HTTPException(
            status_code=404,
            detail="Auth failed"
        )

        # Print exception

    reponse_userinfo = userinfo.json()

    try:
        db_cursor.execute('''SELECT id FROM users WHERE email = %s;''', [response_userinfo.email])

    except Exception as e:
        print("Getting user info from users failed")
        return {"message": str(e)}
    
    try:
        user_info = db_cursor.fetchone()
        user_info_as_json = {"id": user_info[0]}
    except Exception as e:
        print("fetctone() failed")
        return {"message": str(e), "user_info": user_info}
    
    return user_info_as_json



uvicorn.run(app, host="0.0.0.0", port=3000)












