#!/bin/ 

# Install necessary package for virtual environment if not already installed
sudo apt install -y python3.10-venv

# Create project directory and navigate into it
mkdir -p advanced_regression_test_v2 && cd advanced_regression_test_v2

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip and install required packages
pip install --upgrade pip
pip install pytest pytest-html pytest-xdist pytest-mock pytest-cov

# Create the test structure
mkdir -p tests/utils tests/data

# Create a sample utility file
cat <<EOT >> tests/utils/calculations.py
def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    return a / b
EOT

# Create a sample data file with corrected test cases
cat <<EOT >> tests/data/test_data.py
def get_test_cases():
    return [
        {"input": {"a": 2, "b": 3}, "expected": 6},
        {"input": {"a": 5, "b": 0}, "expected_error": "Division by zero is not allowed"},
        {"input": {"a": 10, "b": 2}, "expected": 20},  # Corrected expected value
    ]
EOT

# Create a session-scoped fixture
cat <<EOT >> tests/conftest.py
import pytest
from tests.utils.calculations import multiply, divide

@pytest.fixture(scope="session")
def setup_resources():
    print("Setting up resources for the test session")
    resources = {"status": "initialized"}
    yield resources
    print("Tearing down resources after the test session")
    resources["status"] = "cleaned"
EOT

# Create a more advanced test file
cat <<EOT >> tests/test_advanced_v2.py
import pytest
from tests.utils.calculations import multiply, divide
from tests.data.test_data import get_test_cases

# Test using a session-scoped fixture
def test_fixture_usage(setup_resources):
    assert setup_resources["status"] == "initialized"

# Parameterized test with complex data
@pytest.mark.parametrize("case", get_test_cases())
def test_multiplication_and_division(case):
    a = case["input"]["a"]
    b = case["input"]["b"]

    if "expected_error" in case:
        with pytest.raises(ValueError) as excinfo:
            divide(a, b)
        assert str(excinfo.value) == case["expected_error"]
    else:
        assert multiply(a, b) == case["expected"]

# Custom hook for logging
def pytest_runtest_logreport(report):
    if report.failed:
        print(f"Test {report.nodeid} failed at {report.when} phase.")
    elif report.passed:
        print(f"Test {report.nodeid} passed at {report.when} phase.")
EOT

# Create a script to run tests in parallel with coverage and generate an HTML report
cat <<EOT >> run_advanced_tests_v2.sh
#!/bin/ 
source venv/bin/activate
export PYTHONPATH=\$(pwd)
pytest -n 4 --cov=tests --cov-report=html --html=report.html --self-contained-html --maxfail=1
EOT

# Make the test script executable
chmod +x run_advanced_tests_v2.sh

# Run the test script
./run_advanced_tests_v2.sh

# Output location of the report
echo "Advanced QA Regression Test V2 completed. Report generated at: advanced_regression_test_v2/report.html"
