from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Load the tokenizer and the model
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Move the model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Example text
input_text = "here is a stoy about : "
inputs = tokenizer(input_text, return_tensors="pt").to(device)

# Generate text
outputs = model.generate(**inputs, max_length=50)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
