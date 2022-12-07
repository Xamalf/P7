from fastapi import Cookie, FastAPI, HTTPException
import uvicorn
import psycopg2
from pydantic import BaseModel
from datetime import datetime as dt

app = FastAPI()

class User(BaseModel):
    name: str
    about: str
    email: str

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
    ex_id: int

class ExerciseAndUserName(BaseModel):
    user_name: str
    exercise_name: str

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

db_connection.autocommit = True
db_cursor = db_connection.cursor()

 
@app.post("/data-access/create-user")
async def root(user: User):
    print("create-user entered")

    try:
        db_cursor.execute('''INSERT INTO users(name, about, title, createdAt, email) VALUES (%s, %s, %s, %s, %s);''', [user.name, user.about, "Revuppaal User", dt.now().strftime('%d %B %Y'), user.email])
    except Exception as e:
        print("Creating user in users failed")
        return {"message": str(e)}

    print("create-user exited")
    return {"message": f"{user.name} succesfully created"}


@app.post("/data-access/get-user-info")
async def root(user: UserName, access_token: str = Cookie(None), refresh_token: str = Cookie(None)):

    
    try:
        uauth = userAuth({ "access_token": access_token, "refresh_token": refresh_token })
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail="Auth failed"
        )
    

    try:
        db_cursor.execute('''SELECT u.name, u.title, u.email, u.about, COUNT(ce.user_id), SUM(e.xp) FROM users u JOIN completed_exercises ce ON u.id = ce.user_id JOIN exercises e on ce.ex_id = e.id WHERE u.name = %s GROUP BY u.name, u.title, u.email, u.about;''', [user.name])
    except Exception as e:
        print("Getting user info from users failed")
        return {"message": str(e)}
    
    try:
        user_info = db_cursor.fetchone()
        user_info_as_json = {"name": user_info[0], "title": user_info[1], "email": user_info[2], "about": user_info[3], "completed_exercises": user_info[4], "total_score": user_info[5]}
    except Exception as e:
        print("fetctone() failed")
        return {"message": str(e), "user_info": user_info}

    print("get-user-info exited")

    


    return user_info_as_json


@app.post("/data-access/delete-user")
async def root(user: UserName):
     
    try:
        uauth = userAuth({ "access_token": access_token, "refresh_token": refresh_token })
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail="Auth failed"
        )
    
    try:
        db_cursor.execute('''DELETE FROM users WHERE id = %s''', [user_id])
    except Exception as e:
        print("Deleting user from users failed")
        return {"message": str(e)}
    
    try:
        db_cursor.execute('''DELETE FROM completed_exercises WHERE user_id = %s''', [user_id])
    except Exception as e:
        print("Deleting user from completed_exercises failed")
        return {"message": str(e)}

    print("delete-user exited")
    return {"message": f"User {user.name} succesfully deleted"}
    
# -- #

@app.post("/data-access/get-exercise-description")
async def root(exercise: ExerciseDescription):
    print("get-exercise-description entered")

    try:
        db_cursor.execute('''SELECT * FROM exercises WHERE id = %s''', [exercise.ex_id])
    except Exception as e:
        print("Getting exercise description from exercises failed")
        return {"message": str(e)}

    try:
        exercise_description = db_cursor.fetchone()
    except Exception as e:
        return {"message": str(e)}

    print("get-exercise-description exited")
    return {"description": exercise_description[3], "name": exercise_description[1]}


@app.post("/data-access/insert-completed-exercise")
async def root(exerciseAndUserName: ExerciseAndUserName):
    print("insert-complete-exercise entered")

    try:
        db_cursor.execute('''SELECT id FROM users WHERE name = %s''', [exerciseAndUserName.user_name])
    except Exception as e:
        print("Getting user from users failed")
        return {"message": str(e)}
    
    user_id = db_cursor.fetchone()[0]
    
    try:
        db_cursor.execute('''SELECT id FROM exercises WHERE name = %s''', [exerciseAndUserName.exercise_name])
    except Exception as e:
        print("Getting exercise from exercises failed")
        return {"message": str(e)}

    ex_id = db_cursor.fetchone()[0]

    try:
        db_cursor.execute('''INSERT INTO completed_exercises(ex_id, user_id) VALUES (%s, %s);''', [ex_id, user_id])
    except Exception as e:
        print("Creating user in users failed")
        return {"message": str(e)}
    
    print("insert-complete-exercise exited")
    return {"message": f"User has completed exercise"}


@app.post("/data-access/get-user-scores")
async def root():
    print("get-user-scores entered")
    
    try:
        db_cursor.execute('''SELECT row_number() OVER(ORDER BY SUM(e.xp) DESC) rank, u.name, SUM(e.xp), COUNT(u.name) completed FROM users u JOIN completed_exercises ce ON u.id = ce.user_id JOIN exercises e ON ex_id = e.id GROUP BY u.name ORDER BY SUM DESC;''')
    except Exception as e:
        print("Query failed")
        return {"message": str(e)}
    
    try:
        leaderboard_info = db_cursor.fetchall()
    except Exception as e:
        print("fetchall() failed")
        return {"message": str(e)}

    jsonObject = {}
    for x in leaderboard_info:
        jsonObject.update({x[0] : [x[1], x[2], x[3] ]})
    
    print("get-user-scores exited")
    return jsonObject

uvicorn.run(app, host="0.0.0.0", port=5000)


async def userAuth(token: Token):

    auth_response = requests.post("auth.default:3000/auth/username",
    json=code)

    if auth_response.status_code != 200 or exercise_provider_response.status_code != 200:
        raise HTTPException(
            status_code=404,
            detail="Auth failed"
        )
    
    return auth_response