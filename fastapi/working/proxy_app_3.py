import asyncio
import logging
import aiohttp
import uvicorn
from fastapi import FastAPI, Request
from aiohttp import web

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create the FastAPI app
app = FastAPI()

# Define a route
@app.get("/")
async def hello():
    return {"message": "Hello, world!"}

@app.get("/test")
async def hello():
    return {"message": "Hello, TEST!"}

@app.middleware("http")
async def check_request_prefix(request: Request, call_next):
    root_path = request.scope.get("root_path", "")
    logger.info("Root path: %s", root_path)

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

    return await call_next(request)

# Start the Uvicorn server
async def start_server():
    config = uvicorn.Config(app=app, host="127.0.0.1", port=8000)
    server = uvicorn.Server(config=config)
    await server.serve()

async def main():
    server_task = asyncio.create_task(start_server())

    # Create the reverse proxy
    async def handle(request):
        """
        Acting as a reverse proxy, check and forward the request to the FastAPI server
        """
        proxy_rulez = {
            "/api": "http://127.0.0.1:8000",
        }
        logger.info(request.path)

        # Iterate through the proxy rules, and remove the prefix if it matches.
        # First rule winz.
        for rule in proxy_rulez:
            if (request.path.startswith(rule)):
                request.scope["path"] = request.path[len(rule):]
                request.scope["raw_path"] = b'{scope["path"]}'
                logger.info("Request matches rule: %s, new_path: %s", rule, request.path)


                url = f"http://127.0.0.1:8000{request.path_qs}"
                async with aiohttp.ClientSession() as session:
                    async with session.request(request.method, url) as response:
                        body = await response.read()
                        return web.Response(body=body, status=response.status, headers=response.headers)
            break

        return web.Response(body=b"404 No Rule matched", status=404)

    proxy_app = web.Application()
    proxy_app.router.add_route('*', '/{tail:.*}', handle)

    # Start the reverse proxy server
    runner = web.AppRunner(proxy_app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", 8080)
    await site.start()

    # Send a request to the reverse proxy and print the response
    async with aiohttp.ClientSession() as session:
        async with session.get("http://127.0.0.1:8080/test") as response:
            print(await response.text())
        async with session.get("http://127.0.0.1:8080/api/test") as response:
            print(await response.text())


    # Stop the servers
    await runner.cleanup()
    server_task.cancel()

# Run the event loop
asyncio.run(main())
