from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# Function to run the chat interface
def chat():
    chat_history_ids = None
    for step in range(5):
        new_user_input_ids = tokenizer.encode(input(">> User:") + tokenizer.eos_token, return_tensors='pt')
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids
        chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
        print("DialoGPT: {}".format(tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)))

# Running on different hardware
# Uncomment the configuration you want to use

# CPU Only
# model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium", device_map="auto", device="cpu")

# Single GPU
# model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium", device_map="auto", device="cuda")

# Multiple GPUs
# model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium", device_map="auto", device="cuda:0", torch_dtype=torch.float16, num_gpus=2)

# Apple Silicon (M1/M2)
# model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium", device_map="auto", device="mps")

# Advanced Configuration
# model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium", device_map="auto", device="cuda", max_memory=8*1024**3)

# Start the chat
chat()
