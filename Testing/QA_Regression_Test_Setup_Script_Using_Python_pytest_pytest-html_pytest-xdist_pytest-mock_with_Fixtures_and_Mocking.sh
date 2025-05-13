#!/bin/ 

# Install necessary package for virtual environment if not already installed
sudo apt install -y python3.10-venv

# Create project directory and navigate into it
mkdir -p advanced_qa_regression_test && cd advanced_qa_regression_test

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip and install required packages
pip install --upgrade pip
pip install pytest pytest-html pytest-xdist pytest-mock

# Create tests directory
mkdir -p tests

# Create a sample test file with advanced features
cat <<EOT >> tests/test_advanced.py
import pytest

# Fixture for setup and teardown
@pytest.fixture(scope="module")
def resource_setup_teardown():
    # Setup
    print("Setup: Initializing resource")
    resource = {"status": "initialized"}
    yield resource
    # Teardown
    print("Teardown: Cleaning up resource")
    resource["status"] = "cleaned"

# Parameterized test
@pytest.mark.parametrize("input,expected", [(1, 2), (2, 4), (3, 6)])
def test_multiplication(input, expected):
    assert input * 2 == expected, f"Expected {expected} but got {input * 2}"

# Test using fixture
def test_fixture_usage(resource_setup_teardown):
    assert resource_setup_teardown["status"] == "initialized"

# Example external function for mocking
def external_function():
    return "original"

# Mocking example
def test_mocking(mocker):
    mock_function = mocker.patch(__name__ + ".external_function", return_value="mocked!")
    assert external_function() == "mocked!"
EOT

# Create a script to run tests in parallel and generate an HTML report
cat <<EOT >> run_advanced_tests.sh
#!/bin/ 
source venv/bin/activate
pytest -n 4 --html=report.html --self-contained-html --maxfail=1
EOT

# Make the test script executable
chmod +x run_advanced_tests.sh

# Run the test script
./run_advanced_tests.sh

# Output location of the report
echo "Advanced QA Regression Test completed. Report generated at: advanced_qa_regression_test/report.html"
