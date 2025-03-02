#!/bin/ 

# Update and upgrade the system
sudo apt update && sudo apt upgrade -y

# Install required dependencies
sudo apt install -y git python3 python3-venv python3-pip

# Clone the repository
git clone https://github.com/lm-sys/FastChat.git
cd FastChat

# Set up a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install package and additional requirements
pip install --upgrade pip
pip install -e ".[model_worker,webui]"

# Launch the controller
nohup python3 -m fastchat.serve.controller &

# Wait for the controller to start
sleep 10

# Launch the model worker
nohup python3 -m fastchat.serve.model_worker --model-path lmsys/vicuna-7b-v1.5 &

# Wait for the model worker to start
sleep 10

# Launch the Gradio web server
nohup python3 -m fastchat.serve.gradio_web_server &

# Wait for the Gradio server to start
sleep 10

# Echo the URL to access the application
echo "FastChat application is running. Access it at http://localhost:7860"
