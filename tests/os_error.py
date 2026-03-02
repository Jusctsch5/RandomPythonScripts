
import os

def test_print_os_error():
    print(os.strerror(1))
    print(os.strerror(-1))
    print(os.strerror(2))
    print(os.strerror(20))
    print(os.strerror(200))
    print(os.strerror(2000))

