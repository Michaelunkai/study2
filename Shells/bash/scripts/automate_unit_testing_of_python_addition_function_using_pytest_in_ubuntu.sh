#!/bin/ 

# Create a directory for the project
mkdir -p ~/my_test_project
cd ~/my_test_project

# Update and install necessary tools
sudo apt-get update
sudo apt-get install -y python3 python3-pip

# Install pytest
pip3 install pytest

# Create the Python test script
cat <<EOL > setup_and_run_pytest_scenario_for_simple_addition.py
def add(a, b):
    return a + b

def test_add():
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
EOL

# Create a run script
cat <<EOL > automate_test_scenario_execution_using_pytest_in_ubuntu.sh
#!/bin/ 
pytest setup_and_run_pytest_scenario_for_simple_addition.py
EOL

# Make the run script executable
chmod +x automate_test_scenario_execution_using_pytest_in_ubuntu.sh

# Run the test scenario
./automate_test_scenario_execution_using_pytest_in_ubuntu.sh
