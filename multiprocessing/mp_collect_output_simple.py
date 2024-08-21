from multiprocessing import Process, Queue
import sys
import io

def f(q):
    # Replace sys.stdout with StdoutWrapper
    sys.stdout = StdoutWrapper(q)

    # Original print statement
    print("Hello from child process")

    # Restore sys.stdout to original value after function execution
    sys.stdout = sys.__stdout__

class StdoutWrapper(io.TextIOBase):
    def __init__(self, queue):
        self.queue = queue

    def write(self, data):
        self.queue.put(data)
        # sys.__stdout__.write(data)

    def flush(self):
        pass
        # sys.__stdout__.flush()

if __name__ == '__main__':
    def function():
        print("Hello from parent process")
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    p.join()

    # Print captured output from the queue
    while not q.empty():
        print(q.get(), end='')
