import os
from openai import OpenAI

# Initialize the client with API key directly
client = OpenAI(api_key="api key")

# Initialize conversation history
conversation = [
    {"role": "system", "content": "You are a travel expert for Paris."}
]

# Function to get a response from OpenAI's GPT model
def get_paris_travel_info(question):
    try:
        # Add user question to conversation
        conversation.append({"role": "user", "content": question})
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation
        )
        
        # Add assistant's response to conversation
        assistant_response = response.choices[0].message.content
        conversation.append({"role": "assistant", "content": assistant_response})
        
        return assistant_response
    except Exception as e:
        return f"Error calling OpenAI API: {str(e)}"

# Example usage
question = "What are the must-visit landmarks in Paris?"
answer = get_paris_travel_info(question)
print("Answer from GPT-3.5 Turbo:", answer)
