#!/bin/ 

# This script sets up and runs FastChat with the Vicuna model in Ubuntu on DESKTOP-4IVDSOR.

# Step 1: Install Python 3 and pip3
sudo apt install -y python3 python3-pip

# Step 2: Clone the FastChat repository into /root/FastChat
git clone https://github.com/lm-sys/FastChat.git /root/FastChat
cd /root/FastChat

# Step 3: Install necessary Python packages
pip3 install "fschat[model_worker,webui]"

# Step 4: Run the Vicuna-7B model on CPU only, logging to vicuna.log
nohup python3 -m fastchat.serve.cli --model-path lmsys/vicuna-7b-v1.5 --device cpu > vicuna.log 2>&1 &

# Step 5: Serve the model with Web GUI

# Launch the controller, logging to controller.log
nohup python3 -m fastchat.serve.controller > controller.log 2>&1 &

# Launch the model worker, logging to model_worker.log
nohup python3 -m fastchat.serve.model_worker --model-path lmsys/vicuna-7b-v1.5 > model_worker.log 2>&1 &

# Launch the Gradio web server, logging to web_server.log
nohup python3 -m fastchat.serve.gradio_web_server > web_server.log 2>&1 &

# Wait for a few seconds to ensure that the web server starts
sleep 5

# Echo the URL to access the web interface
echo "FastChat is now running with Vicuna model. Access it via your browser at: http://localhost:7860"
