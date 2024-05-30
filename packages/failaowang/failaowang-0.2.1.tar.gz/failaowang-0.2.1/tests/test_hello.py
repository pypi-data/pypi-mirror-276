# tests/test_hello.py

import unittest
from io import StringIO
import sys
from helloworld.hello import say_hello

class TestHelloWorld(unittest.TestCase):

    def test_say_hello(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        say_hello()
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().strip(), "Hello, World!")

if __name__ == "__main__":
    unittest.main()
