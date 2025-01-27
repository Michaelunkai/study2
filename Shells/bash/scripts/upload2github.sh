#!/bin/bash

# -----------------------------------------------------------------------------
# Script Name: upload.sh
# Description: Uploads a specified file or directory to a GitHub repository.
#              Ensures proper branch tracking and identity configuration.
# Usage: ./upload.sh <file_or_directory_name>
# -----------------------------------------------------------------------------

# Exit immediately if a command exits with a non-zero status
set -e

# ------------------------------- Configuration ------------------------------- #

# GitHub Repository Details
REPO_URL="https://github.com/Michaelunkai/downloadables.git"
REPO_NAME="downloadables"

# Directory where the repository will be cloned or initialized
REPO_DIR="/mnt/c/study/$REPO_NAME"

# Function to clean up the repository directory
cleanup() {
    if [ -d "$REPO_DIR" ]; then
        echo "🧹 Cleaning up temporary repository directory..."
        rm -rf "$REPO_DIR"
        echo "✅ Cleanup completed."
    fi
}

# Trap to ensure cleanup runs on script exit
trap cleanup EXIT

# Function: Print Usage Instructions
print_usage() {
    echo "Usage: $0 <file_or_directory_name>"
    echo "Uploads the specified file or directory to the '$REPO_NAME' GitHub repository."
    exit 1
}

# Function: Initialize a Git repository if needed
initialize_git_repo() {
    if [ ! -d "$REPO_DIR/.git" ]; then
        echo "🔄 Initializing Git repository in '$REPO_DIR'..."
        git init "$REPO_DIR"
        cd "$REPO_DIR" || exit 1
        git remote add origin "$REPO_URL"
        echo "✅ Git repository initialized and remote origin set."
    else
        echo "✅ Git repository already initialized."
        cd "$REPO_DIR" || exit 1
    fi

    # Ensure the correct branch is checked out
    if ! git rev-parse --verify main >/dev/null 2>&1; then
        echo "🔄 Creating and switching to 'main' branch..."
        git checkout -b main
    else
        echo "✅ 'main' branch already exists."
        git checkout main
    fi
}

# Function: Configure Git Identity
configure_git_identity() {
    git config --global user.name "Your Name"
    git config --global user.email "youremail@example.com"
    echo "✅ Git identity configured."
}

# Function: Print Download Commands
print_download_commands() {
    local ITEM_NAME="$1"
    echo
    echo "✅ '$ITEM_NAME' has been successfully uploaded to the repository."
    echo
    echo "🔽 **Download Commands:**"
    echo
    echo "• **wget:**"
    echo "  wget https://raw.githubusercontent.com/Michaelunkai/downloadables/main/$ITEM_NAME"
    echo
    echo "• **PowerShell:**"
    echo "  Invoke-WebRequest -Uri https://raw.githubusercontent.com/Michaelunkai/downloadables/main/$ITEM_NAME -OutFile $ITEM_NAME"
    echo
}

# ------------------------------- Main Script ------------------------------- #

# Ensure exactly one argument is provided
if [ "$#" -ne 1 ]; then
    echo "❌ Error: Invalid number of arguments."
    print_usage
fi

ITEM_NAME="$1"

# Get the absolute path of the file or directory
ITEM_PATH="$(realpath "$ITEM_NAME")"

# Check if the file or directory exists
if [ ! -e "$ITEM_PATH" ]; then
    echo "❌ Error: '$ITEM_NAME' not found at '$ITEM_PATH'."
    exit 1
fi

# Ensure the repository directory exists
if [ ! -d "$REPO_DIR" ]; then
    echo "📂 Creating repository directory '$REPO_DIR'..."
    mkdir -p "$REPO_DIR"
    echo "✅ Repository directory created."
fi

# Initialize the directory as a Git repository and ensure branch setup
initialize_git_repo

# Configure Git identity
configure_git_identity

# Pull the latest changes
echo "🔄 Pulling latest changes from 'main' branch..."
git pull origin main || {
    echo "❌ Error: Failed to pull latest changes."
    exit 1
}
echo "✅ Latest changes pulled successfully."

# Check if the file or directory already exists in the repository
if [ -e "$ITEM_NAME" ]; then
    echo "♻️ File or directory '$ITEM_NAME' already exists in the repository. Replacing it..."
    rm -rf "$ITEM_NAME"
    echo "✅ Existing file or directory removed."
fi

# Copy the new file or directory to the repository
echo "📂 Copying '$ITEM_PATH' to the repository..."
if [ -d "$ITEM_PATH" ]; then
    cp -r "$ITEM_PATH" .
else
    cp "$ITEM_PATH" .
fi
echo "✅ '$ITEM_NAME' copied successfully."

# Add the file or directory to Git
echo "📝 Adding '$ITEM_NAME' to Git..."
git add "$ITEM_NAME" || {
    echo "❌ Error: Failed to add '$ITEM_NAME' to Git."
    exit 1
}
echo "✅ '$ITEM_NAME' added to Git."

# Check if there are any changes to commit
if git diff-index --quiet HEAD --; then
    echo "ℹ️ No changes to commit. Proceeding to push..."
else
    # Commit the changes
    echo "📝 Committing changes..."
    git commit -m "Replace $ITEM_NAME with updated version" || {
        echo "❌ Error: Failed to commit '$ITEM_NAME'."
        exit 1
    }
    echo "✅ Changes committed."
fi

# Push the changes to the remote repository
echo "🚀 Pushing changes to 'main' branch..."
git push -u origin main || {
    echo "❌ Error: Failed to push '$ITEM_NAME' to remote repository."
    exit 1
}
echo "✅ Changes pushed successfully."

# Print download commands
print_download_commands "$ITEM_NAME"

# Explicit cleanup for `/mnt/c/study/downloadables`
echo "🧹 Cleaning up '/mnt/c/study/downloadables'..."
rm -rf /mnt/c/study/downloadables
echo "✅ Cleanup of '/mnt/c/study/downloadables' completed."

# Exit successfully
exit 0
