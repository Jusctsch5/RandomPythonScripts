#!/usr/bin/python3

import functools
import atexit

class CallStack:
    def __init__(self):
        self.stack = []

    def push(self, func_name):
        self.stack.append(func_name)

    def pop(self):
        self.stack.pop()

    def print_call_stack(self):
        self.print_call_stack_recursive(self.stack)

    def print_call_stack_recursive(self, call_stack, indent=''):
        if not call_stack:
            return

        func_name = call_stack[0]
        print(f"{indent}- {func_name}")

        if len(call_stack) > 1:
            self.print_call_stack_recursive(call_stack[1:], indent + '   ')

# Shared instance of CallStack
call_stack_instance = CallStack()

def call_stack():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            call_stack_instance.push(func.__name__)
            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator

# Context manager to print the call stack at the end of 'main'
class CallStackPrinter:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        call_stack_instance.pop()
        self.print_call_stack()

    def register_print_call_stack(self):
        atexit.register(self.print_call_stack)

    def print_call_stack(self):
        call_stack_instance.print_call_stack()

# Example usage
@call_stack()
def fun():
    pass

@call_stack()
def foo():
    pass

@call_stack()
def bar():
    foo()

@call_stack()
def main():
    with CallStackPrinter() as printer:
        fun()
        foo()
        bar()
    printer.register_print_call_stack()

main()
