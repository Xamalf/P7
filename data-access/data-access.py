from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI(root_path="/data-access")

uvicorn.run(app, host="0.0.0.0", port=5000)

@app.post("/create-user")
async def root():
    
    return {"message": f"User succesfully created"}

@app.post("/get-user-info")
async def root():
    
    return {"message": f"Here is the user's info"}

@app.post("/delete-user")
async def root():
    
    return {"message": f"User succesfully deleted"}
    

@app.post("/get-exercise-info")
async def root():
    
    return {"message": f"Here is the exercise info"}

