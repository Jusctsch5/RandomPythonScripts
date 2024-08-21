from dataclasses import dataclass
import sys
import io
import multiprocessing
import functools
from typing import List

@dataclass
class ProcessResult:
    """
    Data class to hold the output of a process
    """
    stdout: List[str]
    stderr: List[str]
    returncode: int

class StdoutWrapper(io.TextIOBase):
    def __init__(self, queue):
        self.queue = queue

    def write(self, data):
        self.queue.put(data)
        # sys.__stdout__.write(data)

    def flush(self):
        pass
        # sys.__stdout__.flush()

class StderrWrapper(io.TextIOBase):
    def __init__(self, queue):
        self.queue = queue

    def write(self, data):
        self.queue.put(data)
        # sys.__stderr__.write(data)

    def flush(self):
        pass
        # sys.__stderr__.flush()

class StreamWrapper(io.TextIOBase):
    def __init__(self, queue):
        self.queue = queue

    def write(self, data):
        self.queue.put(data)

    def flush(self):
        pass

def timeout_decorator(timeout_seconds):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create queues for stdout and stderr
            stdout_queue = multiprocessing.Queue()
            stderr_queue = multiprocessing.Queue()

            # Redirect stdout and stderr to custom wrappers
            sys.stdout = StreamWrapper(stdout_queue)
            sys.stderr = StreamWrapper(stderr_queue)

            try:
                # Run the function in a separate process
                p = multiprocessing.Process(target=func, args=args, kwargs=kwargs)
                p.start()
                p.join(timeout_seconds)

                # Check if process is still alive
                if p.is_alive():
                    p.terminate()
                    p.join()
                    raise TimeoutError(f"Function {func.__name__} timed out after {timeout_seconds} seconds")

            finally:
                # Restore stdout and stderr
                pass

            # Collect output from queues
            stdout_output = []
            stderr_output = []
            while not stdout_queue.empty():
                stdout_output.append(stdout_queue.get())
            while not stderr_queue.empty():
                stderr_output.append(stderr_queue.get())

            return {
                'stdout': ''.join(stdout_output),
                'stderr': ''.join(stderr_output),
            }

        return wrapper

    return decorator

# Example usage
@timeout_decorator(5)
def my_function():
    print("Starting subprocess")
    for i in range(10):
        print(f"Process step {i}")

        if i == 5:
            print("fatal error", file=sys.stderr)
            print("fatal error", file=sys.stderr)

            raise ValueError("Something went wrong")

try:
    result = my_function()
    print("stdout:", result['stdout'])
    print("stderr:", result['stderr'])
    print("Function completed successfully")
except TimeoutError as e:
    print(e)

