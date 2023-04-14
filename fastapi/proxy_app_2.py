from fastapi import APIRouter, FastAPI

# uvicorn proxy_app_2:app --reload
# curl http://localhost/myapp/hello

root_path="/myapp"
prefix_router = APIRouter(prefix=root_path)

app = FastAPI()
app.include_router(prefix_router)

@app.get("/hello")
async def hello():
    return {"message": "Hello, world!"}

