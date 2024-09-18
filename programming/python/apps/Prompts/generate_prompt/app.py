import textwrap

# Function to get user input
def get_user_request():
    user_request = input("Please enter what you want a prompt for: ")
    return user_request

# Function to generate a detailed prompt
def generate_prompt(user_request):
    base_prompt = textwrap.dedent(f"""
        You are an AI specialized in {user_request}. Your role is to act as an expert in this field and respond to queries with detailed, accurate, and helpful information. 
        You should provide insights, solve problems, and offer guidance related to {user_request}. 
        Include specific examples, potential use cases, and important considerations to ensure your responses are comprehensive and useful. 
        Your goal is to be the best possible assistant for tasks and questions related to {user_request}.
    """).strip()
    
    if 'coding' in user_request.lower():
        coding_instruction = "You always create the full code for what you were asked for start to finish, never in snippets, always try to make it as long and advanced as possible but also making sure you creating a working code!!!! always!!! "
        detailed_prompt = base_prompt + "\n\n" + coding_instruction
    else:
        detailed_prompt = base_prompt
    
    return detailed_prompt

# Main function to run the application
def main():
    user_request = get_user_request()
    detailed_prompt = generate_prompt(user_request)
    print("\nGenerated Prompt for AI:\n")
    print(detailed_prompt)

if __name__ == "__main__":
    main()
