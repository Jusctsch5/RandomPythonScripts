import pytest

class TestContextManager:
    def __enter__(self):
        print("Entering context")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Exiting context")
        # Return False to propagate the exception
        return False

def function_that_raises():
    print("function_that_raises")
    raise ValueError("An error occurred")

def test_context_manager_exit_on_exception():
    with pytest.raises(ValueError, match="An error occurred"):
        with TestContextManager():
            function_that_raises()

    print("Done")