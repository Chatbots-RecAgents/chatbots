# test_math_operations.py

import unittest
from chatbot.app2 import add_numbers

class TestAddNumbers(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add_numbers(2, 3), 5)


if __name__ == '__main__':
    unittest.main()
