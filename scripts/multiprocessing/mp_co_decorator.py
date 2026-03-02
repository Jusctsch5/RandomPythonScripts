from multiprocessing import Process, Queue
import sys
import io
import functools

class StdoutWrapper(io.TextIOBase):
    def __init__(self, queue):
        self.queue = queue

    def write(self, data):
        self.queue.put(data)
        # sys.__stdout__.write(data)

    def flush(self):
        pass
        # sys.__stdout__.flush()

def capture_stdout_in_process(timeout=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create a queue for capturing stdout
            q = Queue()

            # Define the target function for the Process
            def target():
                # Replace sys.stdout with StdoutWrapper
                sys.stdout = StdoutWrapper(q)

                # Call the original function
                result = func(*args, **kwargs)

                # Restore sys.stdout to original value
                sys.stdout = sys.__stdout__

                return result

            # Create and start the process
            p = Process(target=target)
            p.start()

            # Wait for the process to finish with timeout
            p.join(timeout)

            # If process is still alive, terminate it
            if p.is_alive():
                p.terminate()
                raise TimeoutError(f"Function {func.__name__} timed out")

            # Print captured output from the queue
            stdout_result = []
            while not q.empty():
                stdout_result.append(q.get())

            return stdout_result

        return wrapper

    return decorator

@capture_stdout_in_process()
def f():
    for i in range(10):
        print(f"Hello from decorated function {i}")

if __name__ == '__main__':
    result = f()
    print(" ".join(result))

