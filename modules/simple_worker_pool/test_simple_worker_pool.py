#
# Copyright 2025. Quantum Corporation. All Rights Reserved.
# Quantum Myriad is either a trademark or registered trademark of
# Quantum Corporation in the US and/or other countries.
#
import asyncio
import pytest
from mgmt.Utilities.simple_worker_pool import SimpleWorkerPool

# Define a simple initializer function
def initializer(worker_arguments, initargs):
    print("initializer", worker_arguments, initargs)
    worker_arguments['init_value'] = initargs[0]

# Define a simple task function that uses the worker arguments
def task_function(x, worker_arguments, y=0):
    return x + worker_arguments['init_value'] + y

@pytest.fixture
def simple_worker_pool():
    # Setup: Create a SimpleWorkerPool with the initializer
    pool = SimpleWorkerPool(
        name="TestPool",
        max_workers=2,
        initializer=initializer,
        initargs=(5,)  # This will set 'init_value' to 5
    )
    yield pool
    # Teardown: Shutdown the pool after tests
    pool.shutdown()

def test_initializer_sets_worker_arguments(simple_worker_pool):
    # Test that the initializer sets the worker arguments correctly
    assert 'init_value' in simple_worker_pool.worker_arguments
    assert simple_worker_pool.worker_arguments['init_value'] == 5

@pytest.mark.asyncio
async def test_simple_worker_pool_arguments(simple_worker_pool):
    # Test that a task can be executed using the worker arguments
    result = await simple_worker_pool.submit_task(task_function, 10)
    assert result == 15  # 10 + 5 (init_value) = 15

    result = await simple_worker_pool.submit_task(task_function, 10, y=10)
    assert result == 25  # 10 + 5 (init_value) + 10 = 25



def task_function_exception(x, worker_arguments, y=0):
    raise Exception("test exception")

@pytest.mark.asyncio
async def test_simple_worker_pool_exception(simple_worker_pool):
    """
    Test to make sure we can handle exceptions in the worker pool.
    """
    try:
        await simple_worker_pool.submit_task(task_function_exception, 10)
    except Exception as e:
        assert str(e) == "test exception"



    return x + worker_arguments['init_value'] + y


@pytest.mark.asyncio
async def test_simple_worker_pool_class_init(simple_worker_pool_class_init):
    result = await simple_worker_pool_class_init.submit_task(task_function, 10)
    assert result == 15  # 10 + 5 (init_value) = 15



class ExampleClass:
    def __init__(self, init_value):
        self.init_value = init_value

    def __del__(self):
        print("__del__", self)

def class_initializer(worker_arguments, initargs):
    print("initializer", worker_arguments, initargs)
    worker_arguments['init_value'] = ExampleClass(initargs[0])

@pytest.fixture
def simple_worker_pool_class_init():
    # Setup: Create a SimpleWorkerPool with the initializer
    pool = SimpleWorkerPool(
        name="TestPool",
        max_workers=2,
        initializer=class_initializer,
        initargs=(5,)  # This will set 'init_value' to 5
    )
    yield pool
    # Teardown: Shutdown the pool after tests
    pool.shutdown()

    import gc
    import weakref
    # Check if ExampleClass instance is garbage collected
    example_instance = pool.worker_arguments['init_value']
    example_weak_ref = weakref.ref(example_instance)
    del example_instance
    gc.collect()  # Force garbage collection

    if example_weak_ref() is not None:
        print("ExampleClass instance was not garbage collected")
        # Debugging: Print referrers
        for ref in gc.get_referrers(pool.worker_arguments['init_value']):
            print(ref)
    assert example_weak_ref() is None, "ExampleClass instance was not garbage collected"


def task_function(x, worker_arguments, y=0):
    return x + worker_arguments['init_value'].init_value + y

@pytest.mark.asyncio
async def test_simple_worker_pool_class_exception(simple_worker_pool_class_init):
    try:
        await simple_worker_pool_class_init.submit_task(task_function_exception, 10)
    except Exception as e:
        assert str(e) == "test exception"


