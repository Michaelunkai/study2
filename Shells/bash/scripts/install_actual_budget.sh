#!/usr/bin/env  

set -e  # Exit immediately if a command exits with a non-zero status

# ============================================
# Function Definitions
# ============================================

# Function to print informational messages
msg_info() {
    echo -e "\e[34m[INFO]\e[0m $1"
}

# Function to print success messages
msg_ok() {
    echo -e "\e[32m[OK]\e[0m $1"
}

# Function to print error messages
msg_error() {
    echo -e "\e[31m[ERROR]\e[0m $1"
}

# ============================================
# Pre-Installation Checks
# ============================================

# Ensure the script is run as root
if [ "$EUID" -ne 0 ]; then
    msg_error "Please run this script as root or using sudo."
    exit 1
fi

# ============================================
# System Update and Upgrade
# ============================================

msg_info "Updating and upgrading the system..."
apt-get update -y && apt-get upgrade -y
msg_ok "System updated and upgraded successfully."

# ============================================
# Install Dependencies
# ============================================

msg_info "Installing required dependencies..."
apt-get install -y \
    curl \
    sudo \
    mc \
    gpg \
    git \
    build-essential \
    systemd
msg_ok "Dependencies installed successfully."

# ============================================
# Set Up Node.js Repository
# ============================================

msg_info "Setting up Node.js repository..."
mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg

echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list
msg_ok "Node.js repository set up successfully."

# ============================================
# Install Node.js and Yarn
# ============================================

msg_info "Installing Node.js and Yarn..."
apt-get update -y
apt-get install -y nodejs
npm install --global yarn
msg_ok "Node.js and Yarn installed successfully."

# ============================================
# Install Actual Budget Application
# ============================================

msg_info "Cloning Actual Budget repository..."
git clone https://github.com/actualbudget/actual-server.git /opt/actualbudget
msg_ok "Repository cloned to /opt/actualbudget."

msg_info "Setting up server files directory..."
mkdir -p /opt/actualbudget/server-files
chown -R root:root /opt/actualbudget/server-files
chmod 755 /opt/actualbudget/server-files
msg_ok "Server files directory set up."

msg_info "Configuring environment variables..."
cat <<EOF > /opt/actualbudget/.env
ACTUAL_UPLOAD_DIR=/opt/actualbudget/server-files
PORT=5006
EOF
msg_ok "Environment variables configured."

msg_info "Installing application dependencies with Yarn..."
cd /opt/actualbudget
yarn install
msg_ok "Actual Budget application installed successfully."

# ============================================
# Create Systemd Service
# ============================================

msg_info "Creating systemd service for Actual Budget..."
cat <<EOF > /etc/systemd/system/actualbudget.service
[Unit]
Description=Actual Budget Service
After=network.target

[Service]
Type=simple
User=root
Group=root
WorkingDirectory=/opt/actualbudget
EnvironmentFile=/opt/actualbudget/.env
ExecStart=/usr/bin/yarn start
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
msg_ok "Systemd service created."

msg_info "Enabling and starting the Actual Budget service..."
systemctl enable --now actualbudget.service
msg_ok "Actual Budget service is active and running."

# ============================================
# Post-Installation Cleanup
# ============================================

msg_info "Cleaning up unnecessary packages and cache..."
apt-get autoremove -y
apt-get autoclean -y
msg_ok "Cleanup completed."

# ============================================
# Launch Browser on Windows
# ============================================

msg_info "Launching Google Chrome on Windows to access Actual Budget..."
# Wait briefly to ensure the service is up
sleep 5
cmd.exe /c start chrome http://localhost:5006
msg_ok "Browser launched successfully."

# ============================================
# Final Message
# ============================================

echo -e "\n\e[32mInstallation of Actual Budget completed successfully! 🎉\e[0m"
echo "You can check the status of the service using:"
echo "  systemctl status actualbudget.service"
