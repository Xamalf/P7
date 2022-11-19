from fastapi import FastAPI, HTTPException
import uvicorn
import psycopg2
from pydantic import BaseModel
from datetime import datetime as dt

app = FastAPI()

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

class UserName(BaseModel):
    name: str

class ExerciseDescription(BaseModel):
    name: str


db_connection = psycopg2.connect(
            database="user_data_db",
            user="user",
            password="passw0rd124",
            host="user-db.default",
            port=5432,
        )

db_cursor = db_connection.cursor()
 
@app.post("/data-access/create-user")
async def root(user: User):
    print("create-user entered")

    db_connection.autocommit = True
    try:
        db_cursor.execute('''INSERT INTO users(name, about, title, createdAt) VALUES (%s, %s, %s, %s);''', [user.name, user.about, "Revuppaal User", dt.now().strftime('%d %B %Y')])
    except Exception as e:
        print("Creating user in users failed")
        return {"message": f'{str(e)}'}

    print("create-user exited")
    return {"message": f"{user.name} succesfully created"}


@app.post("/data-access/get-user-info")
async def root(user: UserName):
    print("get-user-info entered")
    db_connection.autocommit = True

    try:
        db_cursor.execute('''SELECT * FROM users WHERE name = %s''', [user.name])
    except Exception as e:
        print("Getting user info from users failed")
        return {"message": f'{str(e)}'}
    
    try:
        user_info = db_cursor.fetchone()
        user_info_as_json = {"name": user_info[1], "title": user_info[2], "createdAt": user_info[3], "about": user_info[4]}
    except Exception as e:
        print("fetctone() failed")
        return {"message": f'{str(e)}', "user_info": user_info}

    print("get-user-info exited")
    return user_info_as_json


@app.post("/data-access/delete-user")
async def root(user: UserName):
    print("delete-user entered")
    db_connection.autocommit = True

    try:
        db_cursor.execute('''SELECT id FROM users WHERE name = %s''', [user.name])
    except Exception as e:
        print("Getting user from users failed")
        return {"message": f'{str(e)}'}
    
    user_id = db_cursor.fetchone()[0]

    try:
        db_cursor.execute('''DELETE FROM users WHERE id = %s''', [user_id])
    except Exception as e:
        print("Deleting user from users failed")
        return {"message": f'{str(e)}'}
    
    try:
        db_cursor.execute('''DELETE FROM completed_exercises WHERE user_id = %s''', [user_id])
    except Exception as e:
        print("Deleting user from completed_exercises failed")
        return {"message": f'{str(e)}'}

    print("delete-user exited")
    return {"message": f"User {user.name} succesfully deleted"}
    
# -- #

@app.post("/data-access/get-exercise-description")
async def root(exercise: ExerciseDescription):
    print("get-exercise-description entered")
    db_connection.autocommit = True

    try:
        db_cursor.execute('''SELECT description FROM exercises WHERE name = %s''', [exercise.name])
    except Exception as e:
        print("Getting exercise description from exercises failed")
        return {"message": f'{str(e)}'}

    try:
        exercise_description = db_cursor.fetchone()[0]
    except Exception as e:
        return {"message": f'{str(e)}'}

    print("get-exercise-description exited")
    return {"description": exercise_description}






@app.post("/data-access/complete-exercise")
async def root():
    
    return {"message": f"User has completed exercise"}


uvicorn.run(app, host="0.0.0.0", port=5000)