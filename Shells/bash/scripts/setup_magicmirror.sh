#!/usr/bin/env  

# Name: setup_magicmirror.sh
# Description: Script to install MagicMirror on Ubuntu
# Author: Adapted for Ubuntu by Assistant
# License: MIT

# Exit immediately if a command exits with a non-zero status
set -e

# Functions for colored output
function msg_info() {
    echo -e "\033[1;34m[INFO]\033[0m $1"
}

function msg_ok() {
    echo -e "\033[1;32m[OK]\033[0m $1"
}

function msg_error() {
    echo -e "\033[1;31m[ERROR]\033[0m $1"
    exit 1
}

# Check if the script is run as root
if [ "$(id -u)" -ne 0 ]; then
    msg_error "This script must be run as root or with sudo"
fi

# Update and install dependencies
msg_info "Updating system and installing dependencies"
apt-get update && apt-get upgrade -y
apt-get install -y \
  curl \
  sudo \
  mc \
  git \
  ca-certificates \
  gnupg
msg_ok "Dependencies installed"

# Set up Node.js repository
msg_info "Setting up Node.js repository"
mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" >/etc/apt/sources.list.d/nodesource.list
apt-get update
msg_ok "Node.js repository set up"

# Install Node.js
msg_info "Installing Node.js"
apt-get install -y nodejs
msg_ok "Node.js installed"

# Set up MagicMirror repository
msg_info "Setting up MagicMirror repository"
git clone https://github.com/MichMich/MagicMirror /opt/magicmirror
msg_ok "MagicMirror repository set up"

# Install MagicMirror
msg_info "Installing MagicMirror"
cd /opt/magicmirror
npm install --only=prod --omit=dev
msg_ok "MagicMirror installed"

# Configure MagicMirror
msg_info "Configuring MagicMirror"
cat <<EOF >/opt/magicmirror/config/config.js
let config = {
    address: "0.0.0.0",
    port: 8080,
    basePath: "/",
    ipWhitelist: [],
    useHttps: false,
    httpsPrivateKey: "",
    httpsCertificate: "",
    language: "en",
    locale: "en-US",
    logLevel: ["INFO", "LOG", "WARN", "ERROR"],
    timeFormat: 24,
    units: "metric",
    serverOnly: true,
    modules: [
        {
            module: "alert",
        },
        {
            module: "updatenotification",
            position: "top_bar"
        },
        {
            module: "clock",
            position: "top_left"
        },
        {
            module: "calendar",
            header: "US Holidays",
            position: "top_left",
            config: {
                calendars: [
                    {
                        symbol: "calendar-check",
                        url: "webcal://www.calendarlabs.com/ical-calendar/ics/76/US_Holidays.ics"
                    }
                ]
            }
        },
        {
            module: "compliments",
            position: "lower_third"
        },
        {
            module: "weather",
            position: "top_right",
            config: {
                weatherProvider: "openweathermap",
                type: "current",
                location: "New York",
                locationID: "5128581",
                apiKey: "YOUR_OPENWEATHER_API_KEY"
            }
        },
        {
            module: "weather",
            position: "top_right",
            header: "Weather Forecast",
            config: {
                weatherProvider: "openweathermap",
                type: "forecast",
                location: "New York",
                locationID: "5128581",
                apiKey: "YOUR_OPENWEATHER_API_KEY"
            }
        },
        {
            module: "newsfeed",
            position: "bottom_bar",
            config: {
                feeds: [
                    {
                        title: "New York Times",
                        url: "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"
                    }
                ],
                showSourceTitle: true,
                showPublishDate: true,
                broadcastNewsFeeds: true,
                broadcastNewsUpdates: true
            }
        }
    ]
};

/*************** DO NOT EDIT THE LINE BELOW ***************/
if (typeof module !== "undefined") {module.exports = config;}
EOF
msg_ok "MagicMirror configured"

# Create and enable MagicMirror service
msg_info "Creating and enabling MagicMirror service"
cat <<EOF >/etc/systemd/system/magicmirror.service
[Unit]
Description=Magic Mirror
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=root
WorkingDirectory=/opt/magicmirror/
ExecStart=/usr/bin/node serveronly

[Install]
WantedBy=multi-user.target
EOF

systemctl enable --now magicmirror
msg_ok "MagicMirror service created and started"

# Cleanup
msg_info "Cleaning up"
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message
msg_info "MagicMirror installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "MagicMirror is running and accessible at: http://$IP_ADDRESS:8080"
echo "Please replace 'YOUR_OPENWEATHER_API_KEY' in /opt/magicmirror/config/config.js with your OpenWeather API key."
