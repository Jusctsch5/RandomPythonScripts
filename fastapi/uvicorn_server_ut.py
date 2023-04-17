from __future__ import annotations

import asyncio
from typing import List, Optional

import uvicorn


PORT = 8080

class UvicornTestServer(uvicorn.Server):
    """Uvicorn test server

    Usage:
        @pytest.fixture
        server = UvicornTestServer()
        await server.up()
        yield
        await server.down()
    """

    def __init__(self, app, host='127.0.0.1', port=PORT):
        """Create a Uvicorn test server

        Args:
            app (FastAPI): the FastAPI app.
            host (str, optional): the host ip. Defaults to '127.0.0.1'.
            port (int, optional): the port. Defaults to PORT.
        """
        self._startup_done = asyncio.Event()
        self.host = host
        self.port = port
        self.http_endpoint = f"http://{host}:{port}/"
        loop = asyncio.new_event_loop()
        config = uvicorn.Config(app, host=host, port=port, loop=loop)
        super().__init__(config=config)

    async def startup(self, sockets: Optional[List] = None) -> None:
        """
        Override uvicorn startup
        """
        await super().startup(sockets=sockets)
        self._startup_done.set()  # pylint: disable=attribute-defined-outside-init

    async def up(self) -> None:
        """
        Start up server asynchronously
        """
        self._serve_task = asyncio.create_task(self.serve())  # pylint: disable=attribute-defined-outside-init
        await self._startup_done.wait()

    async def down(self) -> None:
        """
        Shut down server asynchronously
        """
        self.should_exit = True
        await self._serve_task

    async def __aenter__(self) -> UvicornTestServer:
        """
        For use as async context manager

        Returns:
            UvicornTestServer: returns this object
        """
        await self.up()
        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        """
        For use as async context manager
        """
        await self.down()
        return None
