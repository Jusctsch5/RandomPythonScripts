import threading
import time

def worker():
    # Simulate some long-running work
    time.sleep(5)  # Sleep for 5 seconds

def main():
    # Create a thread for the worker function
    t = threading.Thread(target=worker)

    # Start the thread
    t.start()

    # Create a timer to abort the thread after a certain time
    timeout = 3  # Timeout in seconds
    timer = threading.Timer(timeout, t.abort)  # Abort the thread after the timeout
    timer.start()

    # Wait for the thread to finish
    t.join()

    # Cancel the timer if the thread finishes before the timeout
    timer.cancel()

if __name__ == "__main__":
    main()
