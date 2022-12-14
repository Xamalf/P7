from fastapi import Cookie, FastAPI, HTTPException
import uvicorn
import psycopg2
from pydantic import BaseModel
from datetime import datetime as dt
import requests
from fastapi.responses import RedirectResponse

app = FastAPI()

class User(BaseModel):
    name: str
    about: str
    email: str

class Exercise(BaseModel):
    name: str
    xp: int
    description: str

class CompletedExerciseWithToken(BaseModel):
    ex_id: str
    access_token: str
    refresh_token: str
class UserName(BaseModel):
    name: str

class ExerciseDescription(BaseModel):
    ex_id: int

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

def userAuth(token: Token):

    auth_response = requests.post("http://auth.default:3000/auth/username",
    json= { "access_token": token.access_token, "refresh_token": token.refresh_token } )

    if auth_response.status_code != 200:
        raise HTTPException(
            status_code=404,
            detail="Auth failed"
        )
    
    return auth_response.json()
 
@app.get("/data-access/create-user")
async def root(username: str = None, email: str = None, about: str = ""):
    print("create-user entered")
    if(username and email):
        try:
            db_cursor.execute('''INSERT INTO users(name, about, title, createdAt, email) VALUES (%s, %s, %s, %s, %s);''', [username, about, "Revuppaal User", dt.now().strftime('%d %B %Y'), email])
        except Exception as e:
            print("Creating user in users failed")
            return {"message": str(e)}

        print("create-user exited")
        return RedirectResponse('/')

    else:
        raise HTTPException(
            status_code=404,
            detail=f"Please fill in the required values"
        )


@app.post("/data-access/get-user-info")
async def root(user: UserName, access_token: str = Cookie(None), refresh_token: str = Cookie(None)):
    print("Get-user-info entered")
    
    try:
        print("I is in try, yes!")
        uauth = userAuth(Token(access_token=access_token, refresh_token=refresh_token))
    except Exception as e:
        print("Le exception :(")
        raise HTTPException(
            status_code=404,
            detail=f"Auth failed {str(e)}"
        )

    
    print("B4 second try")
    try:
        print("Inside 2nd try")
        db_cursor.execute('''SELECT u.name, u.title, u.email, u.about, u.createdat, COUNT(ce.user_id), SUM(e.xp) FROM users u JOIN completed_exercises ce ON u.id = ce.user_id JOIN exercises e on ce.ex_id = e.id WHERE u.name = %s GROUP BY u.name, u.title, u.email, u.about, u.createdat;''', [user.name])
    except Exception as e:
        print("Getting user info from users failed")
        return {"message": str(e)}
    
    print("B4 3rd try")
    try:
        print("Inside 3rd try")
        user_info = db_cursor.fetchone()
        user_info_as_json = {"name": user_info[0], "title": user_info[1], "email": user_info[2], "about": user_info[3], "createdat": user_info[4], "completed_exercises": user_info[5], "total_score": user_info[6]}
    except Exception as e:
        print("fetctone() failed")
        return {"message": str(e), "user_info": user_info}

    print("get-user-info exited")

    


    return user_info_as_json

@app.get("/data-access/user-profile-info")
async def root(access_token: str = Cookie(None), refresh_token: str = Cookie(None)):

    
    try:
        uauth = userAuth(Token(access_token=access_token, refresh_token=refresh_token))
        print(uauth)
    except Exception as e:
        print("uauth failed")
        raise HTTPException(
            status_code=404,
            detail=f"Auth failed + {str(e)}"
        )
    

    try:
        db_cursor.execute('''SELECT u.name, u.title, u.email, u.about, u.createdat, COUNT(ce.user_id), SUM(e.xp) FROM users u JOIN completed_exercises ce ON u.id = ce.user_id JOIN exercises e on ce.ex_id = e.id WHERE u.id = %s GROUP BY u.name, u.title, u.email, u.about, u.createdat;''', [uauth["id"]])
    except Exception as e:
        print("Getting user info from users failed")
        raise HTTPException(
            status_code=404,
            detail=f"Auth failed + {str(e)}"
        )
    
    try:
        user_info = db_cursor.fetchone()
        user_info_as_json = {"name": user_info[0], "title": user_info[1], "email": user_info[2], "about": user_info[3], "createdat": user_info[4], "completed_exercises": user_info[5], "total_score": user_info[6]}
    except Exception as e:
        print("fetctone() failed")
        raise HTTPException(
            status_code=404,
            detail=f"Auth failed + {str(e)}"
        )

    print("get-user-info exited")

    


    return user_info_as_json



@app.post("/data-access/delete-user")
async def root(access_token: str = Cookie(None), refresh_token: str = Cookie(None)):
     
    try:
        uauth = userAuth(Token(access_token=access_token, refresh_token=refresh_token))
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Auth failed + {str(e)}"
        )
    
    try:
        db_cursor.execute('''DELETE FROM users WHERE id = %s''', [uauth["id"]])
    except Exception as e:
        print("Deleting user from users failed")
        return {"message": str(e)}
    
    try:
        db_cursor.execute('''DELETE FROM completed_exercises WHERE user_id = %s''', [uauth["id"]])
    except Exception as e:
        print("Deleting user from completed_exercises failed")
        return {"message": str(e)}

    print("delete-user exited")
    return {"message": f"User succesfully deleted"}
    
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
async def root(completedExerciseandtoken: CompletedExerciseWithToken):
    print("insert-complete-exercise entered")

    try:
        uauth = userAuth(Token(access_token=completedExerciseandtoken.access_token, refresh_token=completedExerciseandtoken.refresh_token))
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Auth failed + {str(e)}"
        )

    try:
        db_cursor.execute('''SELECT * FROM completed_exercises WHERE ex_id = %s AND user_id = %s;''', [completedExerciseandtoken.ex_id, uauth["id"]])
        if not db_cursor.fetchall():
            db_cursor.execute('''INSERT INTO completed_exercises(ex_id, user_id) VALUES (%s, %s);''',
                              [completedExerciseandtoken.ex_id, uauth["id"]])
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


