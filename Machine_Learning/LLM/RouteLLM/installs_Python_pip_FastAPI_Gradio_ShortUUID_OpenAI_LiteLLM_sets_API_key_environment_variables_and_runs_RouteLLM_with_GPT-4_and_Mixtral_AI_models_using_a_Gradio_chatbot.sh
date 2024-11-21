#!/bin/ 

# Step 1: Install Python and pip if not already installed
sudo apt install -y python3 python3-pip

# Step 2: Clone the RouteLLM repository if it doesn't exist
if [ ! -d "RouteLLM" ]; then
    git clone https://github.com/lm-sys/RouteLLM.git
fi
cd RouteLLM

# Step 3: Install the necessary Python packages
pip install fastapi gradio shortuuid openai litellm datasets transformers scikit-learn

# Install PyTorch, TorchVision, and Torchaudio with CUDA 11.1 support
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu111

# Verify PyTorch installation
python3 -c "import torch; print(torch.__version__)"

# Step 4: Set up environment variables (replace with your actual keys)
export OPENAI_API_KEY="sk-XXXXXX"
export ANYSCALE_API_KEY="esecret_XXXXXX"

# Step 5: Run the RouteLLM server
python3 -m routellm.openai_server --routers mf --strong-model gpt-4-1106-preview --weak-model anyscale/mistralai/Mixtral-8x7B-Instruct-v0.1 || {
    echo "Error running RouteLLM server. Please ensure all dependencies are installed and configured correctly."
    exit 1
}

# Step 6: Start a local router chatbot (Optional)
python3 -m examples.router_chat --router mf --threshold 0.11593 || {
    echo "Error running the router chatbot. Please check your network connection and try again."
    exit 1
}

echo "Setup and execution completed successfully."
