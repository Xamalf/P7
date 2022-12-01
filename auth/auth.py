from fastapi import FastAPI, Cookie
import psycopg2
from pydantic import BaseModel
import uvicorn
import requests
app = FastAPI()

class User_info(BaseModel):
    name: str

db_connection = psycopg2.connect(
            database="user_data_db",
            user="user",
            password="passw0rd124",
            host="user-db.default",
            port=5432,
        )

db_cursor = db_connection.cursor()    
db_connection.autocommit = True


@app.get("/auth")
async def root():
    return {"message": "Hello from auth!"}


@app.get("/auth/login")
def root(cookie: str = Cookie(None)):
    print("login entered")
    
    try:
        email = requests.post("http://google-verifier.default:6000/google-verifier/", json={"code": cookie})
    except Exception as e:
        print(f"{str(e)}")

    email = email.content.decode('utf-8')

    print("---------------> " + email)

    db_cursor.execute('''SELECT name, email FROM users WHERE email = %s;''', [email])

    result = db_cursor.fetchone()
    
    if not result:
        print("User NOT authenticated - login exited")
        return False
    else:
        print("User authenticated - login exited")
        return {"name" : result[0], "email" : result[1]}


@app.post("/auth")
async def root(user_info: User_info):
    print(user_info)
    return user_info

uvicorn.run(app, host="0.0.0.0", port=3000)