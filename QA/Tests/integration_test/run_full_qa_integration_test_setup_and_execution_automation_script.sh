#!/bin/bash
set -e

echo "Creating project directory..."
mkdir -p qa_integration_tests/tests

echo "Navigating to project directory..."
cd qa_integration_tests

echo "Creating __init__.py..."
touch tests/__init__.py

echo "Creating sample integration test..."
cat > tests/test_integration.py <<EOF
import pytest

@pytest.fixture(scope="module")
def setup_environment():
    print("Setting up environment...")
    yield
    print("Tearing down environment...")

def test_example_integration(setup_environment):
    assert True == True
EOF

echo "Creating pytest.ini..."
cat > pytest.ini <<EOF
[pytest]
addopts = -v
testpaths = tests
EOF

echo "Running the integration tests..."
pytest

echo "Integration tests completed successfully!"
