#!/bin/bash

# Create project folder and necessary subfolders
mkdir -p ~/qa_professional_unit_tests/tests

# Navigate to the project folder
cd ~/qa_professional_unit_tests

# Create the main application file
cat << 'EOF' > app.py
class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero!")
        return a / b

    def exponentiate(self, base, exponent):
        return base ** exponent

    def modulo(self, a, b):
        if b == 0:
            raise ValueError("Cannot modulo by zero!")
        return a % b
EOF

# Create the test file
cat << 'EOF' > tests/test_calculator.py
import unittest
from app import Calculator
from parameterized import parameterized

class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = Calculator()

    @parameterized.expand([
        ("positive_integers", 2, 3, 5),
        ("negative_integers", -1, -1, -2),
        ("zero_and_integer", 0, 5, 5),
        ("floating_point", 2.5, 2.5, 5.0),
    ])
    def test_add(self, name, a, b, expected):
        result = self.calc.add(a, b)
        self.assertEqual(result, expected, f"Failed {name} case: {a} + {b} != {result}")

    @parameterized.expand([
        ("positive_integers", 10, 5, 5),
        ("negative_integers", -1, -1, 0),
        ("zero_and_integer", 0, 5, -5),
        ("floating_point", 5.5, 2.5, 3.0),
    ])
    def test_subtract(self, name, a, b, expected):
        result = self.calc.subtract(a, b)
        self.assertEqual(result, expected, f"Failed {name} case: {a} - {b} != {result}")

    @parameterized.expand([
        ("positive_integers", 3, 7, 21),
        ("negative_integers", -1, 1, -1),
        ("zero_and_integer", 0, 5, 0),
        ("floating_point", 2.5, 4.0, 10.0),
    ])
    def test_multiply(self, name, a, b, expected):
        result = self.calc.multiply(a, b)
        self.assertEqual(result, expected, f"Failed {name} case: {a} * {b} != {result}")

    @parameterized.expand([
        ("positive_integers", 10, 2, 5),
        ("negative_division", -10, 2, -5),
        ("floating_point", 5.5, 2.2, 2.5),
    ])
    def test_divide(self, name, a, b, expected):
        result = self.calc.divide(a, b)
        self.assertEqual(result, expected, f"Failed {name} case: {a} / {b} != {result}")
        with self.assertRaises(ValueError):
            self.calc.divide(a, 0)

    @parameterized.expand([
        ("positive_integers", 2, 3, 8),
        ("negative_base", -2, 3, -8),
        ("zero_exponent", 5, 0, 1),
        ("floating_point", 2.5, 2, 6.25),
    ])
    def test_exponentiate(self, name, base, exponent, expected):
        result = self.calc.exponentiate(base, exponent)
        self.assertEqual(result, expected, f"Failed {name} case: {base} ** {exponent} != {result}")

    @parameterized.expand([
        ("positive_integers", 10, 3, 1),
        ("negative_divisor", 10, -3, -2),
        ("negative_dividend", -10, 3, 2),
    ])
    def test_modulo(self, name, a, b, expected):
        result = self.calc.modulo(a, b)
        self.assertEqual(result, expected, f"Failed {name} case: {a} % {b} != {result}")
        with self.assertRaises(ValueError):
            self.calc.modulo(a, 0)

    def tearDown(self):
        del self.calc

if __name__ == '__main__':
    unittest.main()
EOF

# Install required packages
pip3 install parameterized

# Run the unit tests
python3 -m unittest discover -s tests -p "test_*.py"
