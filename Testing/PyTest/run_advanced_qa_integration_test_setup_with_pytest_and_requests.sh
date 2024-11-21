#!/bin/ 
set -e

echo "Creating project directory..."
mkdir -p qa_integration_tests/tests

echo "Navigating to project directory..."
cd qa_integration_tests

echo "Creating __init__.py..."
touch tests/__init__.py

echo "Creating advanced integration test..."
cat > tests/test_advanced_integration.py <<EOF
import pytest
import requests

@pytest.fixture(scope="module")
def setup_environment():
    print("Setting up environment...")
    # Example: Setup environment variables or mock services
    yield
    print("Tearing down environment...")

def test_api_response_code(setup_environment):
    response = requests.get('https://jsonplaceholder.typicode.com/posts')
    assert response.status_code == 200, "Expected status code 200"

def test_api_response_content(setup_environment):
    response = requests.get('https://jsonplaceholder.typicode.com/posts/1')
    data = response.json()
    assert data['id'] == 1, "Expected ID to be 1"
    assert 'title' in data, "Expected title in response"
EOF

echo "Creating pytest.ini..."
cat > pytest.ini <<EOF
[pytest]
addopts = -v
testpaths = tests
EOF

echo "Installing necessary packages..."
pip install requests pytest

echo "Running the integration tests..."
pytest

echo "Integration tests completed successfully!"
