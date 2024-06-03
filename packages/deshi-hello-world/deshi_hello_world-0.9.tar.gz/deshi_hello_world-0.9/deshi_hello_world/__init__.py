# hello_world/__init__.py

def hello():
    return "Hello, World!"

def multiply(*args):
    """Multiply multiple numbers and return the result."""
    result = 1
    for num in args:
        result *= num
    return result
