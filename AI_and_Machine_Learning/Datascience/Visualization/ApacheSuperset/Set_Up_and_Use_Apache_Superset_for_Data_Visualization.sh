#!/bin/ 

# Update and upgrade the system
sudo apt update && sudo apt upgrade -y

# Install necessary dependencies
sudo apt install -y python3-pip python3-dev libffi-dev libssl-dev libpq-dev python3-venv

# Create and activate a virtual environment
python3 -m venv superset-venv
source superset-venv/bin/activate

# Install Apache Superset and Flask
pip install apache-superset flask

# Initialize the Superset database
superset db upgrade

# Create an admin user for Superset
export FLASK_APP=superset
superset fab create-admin --username admin --firstname Admin --lastname User --email admin@example.com --password admin

# Load example data into Superset (optional)
superset load_examples

# Initialize Superset roles and permissions
superset init

# Create a superset_config.py with a secure SECRET_KEY
cat <<EOF > superset_config.py
SECRET_KEY = "$(openssl rand -base64 42)"
EOF

# Run Superset in the background
superset run -p 8088 --with-threads --reload --debugger &

# Create a simple Flask application
cat <<EOF > app.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Superset is running!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
EOF

# Run the Flask application
 3 app.py
