#!/bin/ 

# Exit immediately if a command exits with a non-zero status.
set -e

# Variables
USERNAME=$(whoami)
PROJECT_DIR="/home/$USERNAME/label-studio-projects"
SERVICE_FILE="/etc/systemd/system/label-studio.service"

# Install Python 3, pip3, and other dependencies
sudo apt install -y python3 python3-pip python3-venv git

# Install Label Studio globally using pip3
sudo pip3 install label-studio

# Create project directory
mkdir -p "$PROJECT_DIR"

# Create systemd service file for Label Studio
sudo bash -c "cat <<EOF > $SERVICE_FILE
[Unit]
Description=Label Studio Service
After=network.target

[Service]
Type=simple
User=$USERNAME
WorkingDirectory=$PROJECT_DIR
ExecStart=$(which label-studio) start --port 8080
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF"

# Reload systemd to recognize the new service
sudo systemctl daemon-reload

# Start Label Studio service
sudo systemctl start label-studio

# Enable Label Studio service to start on boot
sudo systemctl enable label-studio

# Print status of the Label Studio service
sudo systemctl status label-studio

# Output access information
echo "Label Studio has been installed and started successfully."
echo "Access it by navigating to http://localhost:8080 in your web browser."
