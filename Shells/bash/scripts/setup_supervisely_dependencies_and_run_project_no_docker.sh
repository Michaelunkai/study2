#!/bin/bash

# Script: Install Supervisely Dependencies and Run Project Without Docker
# Purpose: Sets up and runs Supervisely on Ubuntu with all dependencies installed

# Update system packages (without upgrading the system)
echo "Installing dependencies and setting up Supervisely..."

# Install necessary packages
sudo apt install -y \
    curl \
    ca-certificates \
    gnupg \
    lsb-release \
    libssl-dev \
    libffi-dev \
    python3-pip \
    python3-dev \
    build-essential

# Create project directory
PROJECT_DIR="$HOME/supervisely_project"
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

# Install Python dependencies globally (no virtual environment)
pip3 install supervisely

# Create supervisely run script
SUPERVISELY_SCRIPT="$PROJECT_DIR/run_supervisely.sh"

# Add necessary content to run_supervisely.sh
cat <<EOL > $SUPERVISELY_SCRIPT
#!/bin/bash

# Set environment variables (modify according to your need)
export SUPER_USERNAME=admin
export SUPER_PASSWORD=supersecretpassword

# Run Supervisely (assuming supervisely is installed globally)
supervisely --username=\$SUPER_USERNAME --password=\$SUPER_PASSWORD

EOL

# Set executable permissions for the script
chmod +x $SUPERVISELY_SCRIPT

# Run the supervisely project
echo "Running Supervisely..."
$SUPERVISELY_SCRIPT
