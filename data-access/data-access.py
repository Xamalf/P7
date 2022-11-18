from fastapi import FastAPI, HTTPException
import uvicorn
import psycopg2
from pydantic import BaseModel

class User(BaseModel):
    name: str
    about: str 

class Exercise(BaseModel):
    name: str
    xp: int
    description: str

class CompletedExercise(BaseModel):
    ex_id: str
    user_id: str

db_connection = psycopg2.connect(
            database="user_data_db",
            user="user",
            password="passw0rd124",
            host="user-db.default",
            port=5432,
        )
db_cursor = db_connection.cursor()

app = FastAPI()
uvicorn.run(app, host="0.0.0.0", port=5000)
 
@app.post("/data-access/create-user")
async def root(user: User):
    connection.autocommit = True
    
    cursor.execute('''INSERT INTO users(name, about) VALUES (%s, %s);''', user.name, user.about)
    
    return {"message": f"{user.name} succesfully created"}


@app.post("/get-user-info")
async def root():
    
    return {"message": f"Here is the user's info"}

@app.post("/delete-user")
async def root():
    
    return {"message": f"User succesfully deleted"}
    
# -- #

@app.post("/get-exercise-info")
async def root():
    
    return {"message": f"Here is the exercise info"}

@app.post("/complete-exercise")
async def root():
    
    return {"message": f"User has completed exercise"}

