from copy import deepcopy
import logging
from fastapi import FastAPI, Request, Response
import httpx

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create the FastAPI app
api = FastAPI()

@api.get("/")
async def hello():
    return {"message": "Hello, world!"}

@api.get("/test")
async def hello():
    return {"message": "Hello, TEST!"}

@api.middleware("http")
async def check_request_prefix(request: Request, call_next):
    root_path = request.scope.get("root_path", "")
    logger.info("Root path: %s", root_path)
    logger.info("headers: %s", request.headers)
    """
    if "X-Forwarded-For" in request.headers:
        logger.info("Has been forwarded by a reverse proxy: %s", request.url.path)
        # Request has been forwarded by a reverse proxy
        # Do not include the path prefix
        return await call_next(request)

    # Request has not been forwarded by a reverse proxy
    # Include the path prefix
    logger.info("Has not been forwarded by a reverse proxy: %s", request.url.path)
    path = request.url.path
    if not path.startswith("/api"):
        path = "/api" + path
    request.scope["path"] = path
    request.scope["raw_path"] = b'{scope["path"]}'
    """
    return await call_next(request)


proxy = FastAPI()
@proxy.middleware("http")
async def reverse_proxy_middleware(request: Request, call_next) -> Request:
    proxy_rulez = {
        "/api": "http://127.0.0.1:8001",
    }

    logger.info(request.scope["path"])
    path = request.scope["path"]
    logger.info("Request:%s with path: %s", request, path)

    for rule, endpoint in proxy_rulez.items():
        if (path.startswith(rule)):
            new_path = path[len(rule):]
            url = f"{endpoint}{new_path}"
            logger.info("Request:%s matches rule: %s, new url: %s", request, rule, url)
            new_url = url
            new_headers = dict(deepcopy(request.headers))
            new_headers['X-Forwarded-For'] = request.client.host
            new_headers['X-Forwarded-Proto'] = request.url.scheme
            new_headers['X-Forwarded-Prefix'] = rule

            async with httpx.AsyncClient() as client:
                response = await client.request(
                    request.method,
                    new_url,
                    headers=new_headers,
                    content=request.stream())

            headers = response.headers.copy()
            content = await response.aread()
            return Response(content=content, status_code=response.status_code, headers=headers)

    # No matching rule, so just continue
    return await call_next(request)


# uvicorn proxy_app:proxy --reload --port 8000
# uvicorn proxy_app:api --reload --port 8001
# curl http://localhost:8000/api/ # 200
# curl http://localhost:8000/api/test # 200
# curl http://localhost/test # 404
