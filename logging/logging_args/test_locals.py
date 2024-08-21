def log_args(func):
    def wrapper(*args, **kwargs):
        arg_dict = {}
        for i, arg in enumerate(args):
            arg_dict[func.__code__.co_varnames[i]] = str(arg)
        for k, v in kwargs.items():
            arg_dict[k] = str(v)

        span_name = ""
        if func.__code__.co_varnames[0] == 'self':
            span_name = type(args[0]).__name__ + "." + func.__name__
        elif func.__code__.co_varnames[0] == 'cls':
            span_name = args[0].__name__ + "." + func.__name__
        else:
            span_name = func.__name__
        print(f"Function {span_name} called with arguments: {arg_dict}")
        return func(*args, **kwargs)
    return wrapper

@log_args
def example_function(x, y, z=10):
    return 10

class Square:
    def __init__(self, side):
        self.side = side

    @log_args
    def area(self):
        return self.side * self.side

    @classmethod
    @log_args
    def class_area(cls, x):
        return x*x

    @staticmethod
    @log_args
    def static_area(x):
        return x*x


example_function(1, 2, z=3)

s = Square(5)
s.area()

Square.class_area(2)

Square.static_area(2)
