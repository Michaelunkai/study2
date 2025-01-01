#!/bin/ 

# Step 1: Install python3-venv
sudo apt install -y python3.10-venv

# Step 2: Create and navigate to the project folder
mkdir -p ~/qa_exploratory_test && cd ~/qa_exploratory_test

# Step 3: Initialize a new Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Step 4: Install required testing tools
pip install --upgrade pip
pip install pytest pytest-xdist allure-pytest

# Step 5: Create pytest.ini to register the custom mark
cat <<EOT >> pytest.ini
[pytest]
markers =
    exploratory: marker for exploratory tests
EOT

# Step 6: Create test structure
mkdir -p tests
touch tests/__init__.py
cat <<EOT >> tests/test_sample.py
import pytest

@pytest.mark.exploratory
def test_example():
    assert 1 == 1

@pytest.mark.exploratory
def test_advanced():
    assert "QA" in "QA exploratory testing"
EOT

# Step 7: Run the tests with pytest and generate allure reports
pytest --alluredir=allure-results tests/

# Step 8: Download, unzip, and run Allure command line tool
wget https://github.com/allure-framework/allure2/releases/download/2.17.2/allure-2.17.2.zip && unzip allure-2.17.2.zip && cd allure-2.17.2/bin && ./allure serve ~/qa_exploratory_test/allure-results

# Step 9: Deactivate the virtual environment
deactivate
