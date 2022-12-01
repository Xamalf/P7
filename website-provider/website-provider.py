from fastapi import FastAPI
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI(root_path="/")

app.mount("/", StaticFiles(directory="dist", html=True), name="frontend")

@app.exception_handler(404)
def exception_404(input1, input2):
    return RedirectResponse('/')


uvicorn.run(app, host="0.0.0.0", port=4000)
