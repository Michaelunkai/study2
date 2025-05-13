#!/bin/ 

# =============================================================================
# Script Name: automate_nodemon_setup_and_run_with_all_dependencies.sh
# Description: Automates the installation and configuration of Node.js, npm,
#              and Nodemon on Ubuntu. Initializes a new Node.js project,
#              sets up necessary configuration files, and starts the application
#              with Nodemon monitoring for changes.
# Author: OpenAI ChatGPT
# Date: 2024-09-20
# =============================================================================

# Exit immediately if a command exits with a non-zero status
set -e

# ---------------------------- Function Definitions --------------------------

# Function to display messages
function echo_info {
    echo -e "\e[34m[INFO]\e[0m $1"
}

function echo_success {
    echo -e "\e[32m[SUCCESS]\e[0m $1"
}

function echo_error {
    echo -e "\e[31m[ERROR]\e[0m $1"
}

# ---------------------------- Begin Script Execution ------------------------

echo_info "Starting Nodemon setup and project initialization..."

# ---------------------------- Update and Install Node.js ---------------------

echo_info "Installing Node.js and npm via NodeSource repository..."

# Install curl if not already installed
if ! command -v curl &> /dev/null
then
    echo_info "curl not found. Installing curl..."
    sudo apt-get install -y curl
fi

# Add NodeSource repository for Node.js LTS version
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -

# Install Node.js and npm
sudo apt-get install -y nodejs

# Verify installation
echo_info "Verifying Node.js and npm installation..."
node_version=$(node -v)
npm_version=$(npm -v)
echo_success "Node.js version: $node_version"
echo_success "npm version: $npm_version"

# ---------------------------- Initialize npm Project ------------------------

echo_info "Initializing a new npm project with default settings..."
npm init -y

echo_success "npm project initialized."

# ---------------------------- Install Nodemon -------------------------------

echo_info "Installing Nodemon as a development dependency..."
npm install --save-dev nodemon

echo_success "Nodemon installed successfully."

# ---------------------------- Create nodemon.json --------------------------

echo_info "Creating nodemon.json configuration file..."

cat <<EOL > nodemon.json
{
  "watch": ["src"],
  "ext": "js,json",
  "exec": "node src/app.js",
  "env": {
    "NODE_ENV": "development"
  }
}
EOL

echo_success "nodemon.json created."

# ---------------------------- Create Project Structure ----------------------

echo_info "Creating project directory structure..."

mkdir -p src

echo_success "Project directories created."

# ---------------------------- Create Sample app.js --------------------------

echo_info "Creating sample app.js file..."

cat <<EOL > src/app.js
const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// Sample route
app.get('/', (req, res) => {
    res.send('Hello, Nodemon is running!');
});

// Start the server
app.listen(PORT, () => {
    console.log(\`Server is running on port \${PORT}\`);
});
EOL

echo_success "src/app.js created."

# ---------------------------- Install Express -------------------------------

echo_info "Installing Express.js framework..."

npm install express

echo_success "Express.js installed successfully."

# ---------------------------- Update package.json Scripts --------------------

echo_info "Updating package.json with development script..."

# Use jq to modify package.json. Install jq if not present.
if ! command -v jq &> /dev/null
then
    echo_info "jq not found. Installing jq..."
    sudo apt-get install -y jq
fi

# Add "dev" script using jq
jq '.scripts.dev = "nodemon"' package.json > temp_package.json && mv temp_package.json package.json

echo_success "package.json scripts updated."

# ---------------------------- Start the Application -------------------------

echo_info "Starting the Node.js application with Nodemon..."

# Start Nodemon
npx nodemon

# =============================================================================
# End of Script
# =============================================================================
