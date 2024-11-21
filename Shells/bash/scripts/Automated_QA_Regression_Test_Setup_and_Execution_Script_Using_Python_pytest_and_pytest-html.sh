#!/bin/ 

# Create project directory and navigate into it
mkdir -p qa_regression_test && cd qa_regression_test

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip and install required packages
pip install --upgrade pip
pip install pytest pytest-html

# Create tests directory
mkdir -p tests

# Create a sample test file
cat <<EOT >> tests/test_sample.py
import pytest

def test_example_1():
    assert 1 + 1 == 2

def test_example_2():
    assert "hello".upper() == "HELLO"
EOT

# Create a script to run tests and generate HTML report
cat <<EOT >> run_tests.sh
#!/bin/ 
source venv/bin/activate
pytest --html=report.html --self-contained-html
EOT

# Make the test script executable
chmod +x run_tests.sh

# Run the test script
./run_tests.sh

# Output location of the report
echo "QA Regression Test completed. Report generated at: qa_regression_test/report.html"
