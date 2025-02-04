import pytest
import asyncio
from concurrent.futures import ThreadPoolExecutor

class Resource:
    def __init__(self):
        pass

    def use(self):
        print("Resource.use")

    def __del__(self):
        print("Resource.__del__")

class TestContextManager:
    def __enter__(self):
        print("Entering context")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Exiting context")
        # Return False to propagate the exception
        return False

def function_that_raises():
    with TestContextManager():
        resource = Resource()
        raise ValueError("An error occurred")

async def async_function_with_context():
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor(max_workers=1) as executor:
        await loop.run_in_executor(executor, function_that_raises)

@pytest.mark.asyncio
async def test_context_manager_exit_on_exception_with_threadpool():
    with pytest.raises(ValueError, match="An error occurred"):
        await async_function_with_context()
