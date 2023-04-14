import asyncio
from contextlib import asynccontextmanager
from contextvars import copy_context, ContextVar
import uuid

client_context = ContextVar("client")

clients = 10
requests = 32

class Request():
    def __init__(self, producer_i, id):
        self.producer_i = producer_i
        self.id = id

    def __repr__(self):
        return f"Request id:{self.id} producer:{self.producer_i}"

class Client():
    def __init__(self, index, settings):
        self.index = index
        self.settings = settings

    async def process_request(self, consumer, request):
        print(f"client:{self.index}, consumer:{consumer} request:{request}")
        # time.sleep(1)
        await asyncio.sleep(1)

@asynccontextmanager
async def create_client_context(client_queue):
    # Initialization process
    client = await client_queue.get()
    client_context.set(client)
    try:
        # Yield the current context which is set up.
        yield copy_context()
    finally:
        await client_queue.put(client)

async def producer(p_i, request_queue):
    for i in range(10):
        # produce a token and send it to a consumer
        await request_queue.put(Request(p_i, uuid.uuid4()))
        await asyncio.sleep(2)


async def consumer(c_i, client_queue, requests_queue):
    while True:
        request = await requests_queue.get()
        async with create_client_context(client_queue) as app_ctx:
            await app_ctx[client_context].process_request(c_i, request)

async def request_processer():
    client_queue = asyncio.Queue()
    requests_queue = asyncio.Queue()

    settings = {"client_settings"}
    for i in range(clients):
        client_queue.put_nowait(Client(i, settings))
    consumers = [asyncio.create_task(consumer(x, client_queue, requests_queue))
                 for x in range(20)]
    producers = [asyncio.create_task(producer(y, requests_queue))
                 for y in range(1)]

    await asyncio.gather(*producers)
    print('---- done producing')

    await requests_queue.join()

asyncio.run(request_processer())

