from fastapi import FastAPI, Request
from http import HTTPStatus
from starlette.responses import RedirectResponse, PlainTextResponse, FileResponse, Response, JSONResponse

# uvicorn proxy_app:app --reload

app = FastAPI(root_path="/proxy")

@app.route("/query", methods=["GET"])
async def query(request: Request):
    return RedirectResponse("/proxy/login", status_code=HTTPStatus.TEMPORARY_REDIRECT)

@app.route("/login", methods=["GET"])
async def login(request: Request):
    return JSONResponse({"message": "Welcome to the login page!"})



