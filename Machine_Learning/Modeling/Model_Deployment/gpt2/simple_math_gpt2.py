from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import re

# Load the tokenizer and the model
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Move the model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Function to generate a conversational response
def generate_response(input_text, past=None):
    # Encode the input text
    inputs = tokenizer(input_text, return_tensors="pt").to(device)
    
    # Generate response, keeping track of the conversation history
    outputs = model.generate(
        **inputs,
        max_length=100,
        pad_token_id=tokenizer.eos_token_id,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.7,
        past_key_values=past,
    )
    
    # Decode and return the response along with the updated past
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Function to handle specific queries like math operations
def handle_specific_queries(user_input):
    # Check if the input is a simple math question
    math_query = re.match(r'(\d+)\s*([+\-*/x])\s*(\d+)', user_input)
    if math_query:
        num1 = int(math_query.group(1))
        operator = math_query.group(2)
        num2 = int(math_query.group(3))
        
        if operator == '+' or operator == 'plus':
            return str(num1 + num2)
        elif operator == '-' or operator == 'minus':
            return str(num1 - num2)
        elif operator == '*' or operator == 'x' or operator == 'times':
            return str(num1 * num2)
        elif operator == '/' or operator == 'divided by':
            if num2 != 0:
                return str(num1 / num2)
            else:
                return "Cannot divide by zero."
    
    # For other queries, return None to use GPT-2 model
    return None

# Initialize conversation history
conversation_history = ""

# Start a simple conversation loop
while True:
    user_input = input("User: ")
    
    # First, try to handle specific queries
    specific_response = handle_specific_queries(user_input)
    
    if specific_response:
        response = specific_response
    else:
        # Prepend the conversation history to the current user input
        conversation_input = conversation_history + " " + user_input
        
        # Generate the model's response
        response = generate_response(conversation_input)
    
    # Print and store the response
    print("Bot:", response)
    
    # Update conversation history
    conversation_history += " " + user_input + " " + response
    
    # Optional: Limit conversation history length
    conversation_history = conversation_history[-1000:]
