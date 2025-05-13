#!/bin/  
# Function to check if a command exists
command_exists() {
    command -v "$1" &> /dev/null
}
# Update system and install dependencies
if ! command_exists curl; then
    echo "Installing curl..."
    sudo apt update && sudo apt install -y curl
else
    echo "curl is already installed. Skipping..."
fi
# Install nvm and Node.js if not already installed
export NVM_DIR="$HOME/.nvm"
if [ ! -d "$NVM_DIR" ]; then
    echo "Installing nvm..."
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
    source $NVM_DIR/nvm.sh
    source $NVM_DIR/ _completion
else
    echo "nvm is already installed. Skipping..."
    source $NVM_DIR/nvm.sh
    source $NVM_DIR/ _completion
fi
# Install latest LTS version of Node.js if not already installed
if ! command_exists node; then
    echo "Installing Node.js..."
    nvm install --lts
    nvm use --lts
else
    echo "Node.js is already installed. Skipping..."
fi
# Update npm if it's not the latest version
if npm outdated -g npm | grep -q npm; then
    echo "Updating npm..."
    npm install -g npm@latest
else
    echo "npm is already up to date. Skipping..."
fi
# Install ai-renamer if not already installed
if ! command_exists ai-renamer; then
    echo "Installing ai-renamer..."
    npm install -g ai-renamer --yes
else
    echo "ai-renamer is already installed. Skipping..."
fi
# Install Ollama if not already installed
if ! command_exists ollama; then
    echo "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sudo sh
else
    echo "Ollama is already installed. Skipping..."
fi
# Start Ollama service
echo "Starting Ollama service..."
sudo systemctl start ollama
# Pull the llama3 model if not already pulled
if ! ollama list | grep -q llama3; then
    echo "Pulling llama3 model..."
    ollama pull llama3
else
    echo "llama3 model is already pulled. Skipping..."
fi
# Wait for Ollama to start and model to be ready
echo "Waiting for Ollama to start and model to be ready..."
sleep 30
# Run ai-renamer with increased memory allocation
echo "Running ai-renamer..."
NODE_OPTIONS="--max-old-space-size=8192" npx ai-renamer /mnt/c/Users/micha/Downloads --provider=ollama --model=llama3 --case=snakeCase --chars=25 --include-subdirectories=true
echo "Script completed." 
