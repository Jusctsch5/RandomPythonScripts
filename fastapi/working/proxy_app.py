from fastapi import FastAPI, Request
from http import HTTPStatus
from starlette.responses import RedirectResponse, PlainTextResponse, FileResponse, Response, JSONResponse

# uvicorn proxy_app:app --reload

app = FastAPI(root_path="/api")

# Define a route
@app.get("/")
async def hello():
    return {"message": "Hello, world!"}

@app.get("/test")
async def hello():
    return {"message": "Hello, TEST!"}
