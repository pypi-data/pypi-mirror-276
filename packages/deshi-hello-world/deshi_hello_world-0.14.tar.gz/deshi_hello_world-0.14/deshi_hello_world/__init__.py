# hello_world/__init__.py

def hello():
    return "Hello, World!"

def multiply1(*numbers):
    """Multiply multiple numbers and return the result."""
    result = 1
    for num in numbers:
        result *= num
    return result
