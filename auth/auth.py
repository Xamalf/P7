from fastapi import FastAPI, Cookie
import psycopg2
from pydantic import BaseModel
import uvicorn

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
    
    email = "Kasper"
    # email = kald google verifier på cookie
    db_cursor.execute('''SELECT 1 FROM users WHERE name = %s;''', [email])

    result = db_cursor.fetchone()
    
    if not result:
        print("login exited")
        return {"result": "False"} # False
    else:
        print("login exited")
        return {"result": "True"} # True


@app.post("/auth")
async def root(user_info: User_info):
    print(user_info)
    return user_info

uvicorn.run(app, host="0.0.0.0", port=3000)