#!/bin/ 

# Script to set up and run the Foundry Ethereum toolkit with Rust in Ubuntu

# Install Rust and required dependencies
sudo apt install -y curl build-essential libssl-dev pkg-config

# Install Rust using rustup
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Add Rust to PATH
source $HOME/.cargo/env

# Clone the Foundry repository
git clone https://github.com/foundry-rs/foundry.git
cd foundry

# Build the Foundry project with a retry mechanism for large projects
attempt=0
max_attempts=3
until [ "$attempt" -ge "$max_attempts" ]
do
   cargo build --release && break
   attempt=$((attempt+1))
   echo "Build failed, retrying ($attempt/$max_attempts)..."
done

if [ "$attempt" -ge "$max_attempts" ]; then
    echo "Build failed after $max_attempts attempts."
    exit 1
fi

# Add Foundry binaries to PATH for this session
export PATH="$PATH:$HOME/foundry/target/release"

# Initialize a new Foundry project
forge init my-foundry-project
cd my-foundry-project

# Compile the contracts and run tests
forge build
forge test

# Run the local Ethereum node using Anvil
anvil
