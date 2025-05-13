#!/bin/ 

# Create project folder and necessary subfolders
mkdir -p ~/qa_advanced_unit_tests/tests

# Navigate to the project folder
cd ~/qa_advanced_unit_tests

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

class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = Calculator()

    def test_add(self):
        self.assertEqual(self.calc.add(2, 3), 5)
        self.assertEqual(self.calc.add(-1, 1), 0)
        self.assertEqual(self.calc.add(-1, -1), -2)

    def test_subtract(self):
        self.assertEqual(self.calc.subtract(10, 5), 5)
        self.assertEqual(self.calc.subtract(-1, 1), -2)
        self.assertEqual(self.calc.subtract(-1, -1), 0)

    def test_multiply(self):
        self.assertEqual(self.calc.multiply(3, 7), 21)
        self.assertEqual(self.calc.multiply(-1, 1), -1)
        self.assertEqual(self.calc.multiply(-1, -1), 1)

    def test_divide(self):
        self.assertEqual(self.calc.divide(10, 2), 5)
        self.assertEqual(self.calc.divide(-1, 1), -1)
        self.assertEqual(self.calc.divide(-1, -1), 1)
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)

    def test_exponentiate(self):
        self.assertEqual(self.calc.exponentiate(2, 3), 8)
        self.assertEqual(self.calc.exponentiate(5, 0), 1)
        self.assertEqual(self.calc.exponentiate(-2, 3), -8)

    def test_modulo(self):
        self.assertEqual(self.calc.modulo(10, 3), 1)
        self.assertEqual(self.calc.modulo(10, -3), -2)  # Corrected expectation
        self.assertEqual(self.calc.modulo(-10, 3), 2)
        with self.assertRaises(ValueError):
            self.calc.modulo(10, 0)

    def tearDown(self):
        del self.calc

if __name__ == '__main__':
    unittest.main()
EOF

# Run the unit tests
python3 -m unittest discover -s tests -p "test_*.py"
