#!/bin/ 

# Step 1: Update and Install Dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install -y git python3 python3-pip

# Step 2: Shallow Clone the Repository with Retry Logic
REPO_URL="https://github.com/oobabooga/text-generation-webui.git"
CLONE_DIR="text-generation-webui"

# Retry logic: attempt up to 3 times
for i in {1..3}; do
    echo "Attempting to shallow clone the repository (Attempt $i)..."
    git clone --depth 1 $REPO_URL $CLONE_DIR && break
    if [ "$i" -eq 3 ]; then
        echo "Failed to clone the repository after 3 attempts."
        exit 1
    fi
    echo "Retrying in 5 seconds..."
    sleep 5
done

# Step 3: Navigate to the Project Directory
cd $CLONE_DIR || { echo "Failed to enter directory $CLONE_DIR"; exit 1; }

# Step 4: Set Up the Environment
python3 -m venv venv
source venv/bin/activate

# Step 5: Install Python Dependencies
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Exiting..."
    exit 1
fi

# Step 6: Start the Web UI
if [ -f "server.py" ]; then
      server.py &
    echo "Web UI is running. Access it at http://localhost:7860"
else
    echo "server.py not found. Exiting..."
    exit 1
fi
