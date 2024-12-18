#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Variables
INSTALL_USER="ubuntu"  # Change this if your target user is different
BASHRC_PATH="/home/$INSTALL_USER/.bashrc"
BREW_INSTALL_SCRIPT_URL="https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh"
BREW_SHELLENV_COMMAND="/home/linuxbrew/.linuxbrew/bin/brew shellenv"

# Function to print messages
print_message() {
    echo "========================================"
    echo "$1"
    echo "========================================"
}

# Function to check if a user exists
check_user_exists() {
    if id "$1" &>/dev/null; then
        return 0
    else
        echo "User '$1' does not exist. Please create the user or specify an existing one."
        exit 1
    fi
}

# Function to install Homebrew as the specified user
install_homebrew() {
    print_message "Installing Homebrew as user '$INSTALL_USER'..."

    # Run the Homebrew installation script as the target user
    sudo -u "$INSTALL_USER" /bin/bash -c "$(curl -fsSL $BREW_INSTALL_SCRIPT_URL)"

    print_message "Homebrew installation script executed."
}

# Function to update .bashrc with Homebrew environment variables
update_bashrc() {
    print_message "Updating $BASHRC_PATH with Homebrew environment variables..."

    # Append the brew shellenv command to .bashrc if it's not already present
    if ! grep -q 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' "$BASHRC_PATH"; then
        echo '' >> "$BASHRC_PATH"
        echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> "$BASHRC_PATH"
        echo "Added Homebrew environment to $BASHRC_PATH"
    else
        echo "Homebrew environment already exists in $BASHRC_PATH"
    fi
}

# Function to source the updated .bashrc
source_bashrc() {
    print_message "Sourcing $BASHRC_PATH to apply changes..."

    # Source the .bashrc file to update the current shell session
    source "$BASHRC_PATH"

    print_message "Environment variables updated."
}

# Main Execution Flow

# Check if the script is run as root or with sudo
if [[ "$EUID" -ne 0 ]]; then
    echo "Please run this script with sudo or as root."
    exit 1
fi

# Check if the target user exists
check_user_exists "$INSTALL_USER"

# Install Homebrew
install_homebrew

# Wait for a short period to ensure installation completes
sleep 10

# Update .bashrc with Homebrew's environment variables
update_bashrc

# Source the updated .bashrc
source_bashrc

# Verify Homebrew installation
print_message "Verifying Homebrew installation..."
sudo -u "$INSTALL_USER" /bin/bash -c "brew --version"

print_message "Homebrew installation completed successfully!"
