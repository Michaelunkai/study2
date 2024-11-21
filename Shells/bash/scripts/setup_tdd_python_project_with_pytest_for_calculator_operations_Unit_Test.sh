#!/bin/ 

# Create the project directory and navigate into it
mkdir -p ~/tdd_calculator_example && cd ~/tdd_calculator_example

# Install Python and pip
sudo apt install -y python3 python3-pip

# Install pytest for running tests
pip3 install --user pytest

# Create the test file with proper imports
cat <<EOL > test_calculator.py
import pytest
from calculator import addition, subtraction, multiplication, division

def test_addition():
    assert addition(2, 3) == 5

def test_subtraction():
    assert subtraction(5, 3) == 2

def test_multiplication():
    assert multiplication(4, 3) == 12

def test_division():
    assert division(10, 2) == 5
EOL

# Create the implementation file
cat <<EOL > calculator.py
def addition(a, b):
    return a + b

def subtraction(a, b):
    return a - b

def multiplication(a, b):
    return a * b

def division(a, b):
    return a / b
EOL

# Run the tests
pytest
