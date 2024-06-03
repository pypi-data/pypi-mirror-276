# tests/test_hello_world.py
from hello_world import hello

def test_hello():
    assert hello() == "Hello, World!"
