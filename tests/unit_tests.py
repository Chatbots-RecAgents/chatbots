# tests/test_my_code.py
from chatbot.app2 import add_numbers

def test_add_numbers():
    assert add_numbers(2, 3) == 5
    assert add_numbers(-2, 3) == 1
    assert add_numbers(-2, -3) == -5
