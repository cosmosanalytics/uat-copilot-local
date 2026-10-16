"""
test_math_engine.py
Automated test suite using standard unittest and pytest compatible runner.
"""

import unittest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from math_engine import add, multiply, divide, compute_compound_interest

class TestMathEngine(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(0, 0), 0)

    def test_multiply(self):
        self.assertEqual(multiply(3, 4), 12)
        self.assertEqual(multiply(-2, 3), -6)
        self.assertEqual(multiply(5, 0), 0)

    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)
        self.assertEqual(divide(9, 3), 3)
        with self.assertRaises(ZeroDivisionError):
            divide(10, 0)

    def test_compound_interest(self):
        # $1000 at 5% for 3 years: 1000 * (1.05)^3 = 1157.63
        self.assertEqual(compute_compound_interest(1000, 0.05, 3), 1157.63)
        with self.assertRaises(ValueError):
            compute_compound_interest(-100, 0.05, 1)

if __name__ == '__main__':
    unittest.main()
