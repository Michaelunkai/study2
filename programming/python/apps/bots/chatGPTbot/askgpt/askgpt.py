#!/usr/bin/env python3

import argparse
import os
import sys
import logging
import readline  # For command history and auto-completion
import openai
import subprocess

# Initialize logging
log_file = os.path.expanduser('~/askgpt.log')
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_command_from_gpt(prompt):
    # Load the API key from environment variables
    api_key = os.getenv('ASK_API_KEY')

    # Check API key
    if not api_key:
        print("API key not found in environment variables.")
        sys.exit(1)

    # Set up the OpenAI API client
    openai.api_key = api_key

    # Prepare the messages for the chat completion
    messages = [
        {"role": "system", "content": "As a Linux terminal helper, generate safe and efficient Linux commands based on the user's request. Format the answer as just the command in one line without any delimiters."},
        {"role": "user", "content": prompt}
    ]

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )
        command = completion.choices[0].message.content.strip()
        logging.info(f"Generated command: {command}")
        return command
    except Exception as e:
        logging.error(f"An error occurred while getting command: {e}")
        print(f"An error occurred: {e}")
        sys.exit(1)

def get_explanation_from_gpt(command):
    # Load the API key from environment variables
    api_key = os.getenv('ASK_API_KEY')

    # Check API key
    if not api_key:
        print("API key not found in environment variables.")
        sys.exit(1)

    # Set up the OpenAI API client
    openai.api_key = api_key

    # Prepare the messages for the chat completion
    messages = [
        {"role": "system", "content": "You are a Linux expert. Explain in detail what the following command does."},
        {"role": "user", "content": command}
    ]

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )
        explanation = completion.choices[0].message.content.strip()
        logging.info(f"Generated explanation: {explanation}")
        return explanation
    except Exception as e:
        logging.error(f"An error occurred while getting explanation: {e}")
        print(f"An error occurred: {e}")
        sys.exit(1)

def is_command_safe(command):
    dangerous_commands = ['rm -rf', 'mkfs', 'dd if=', ':() { :|: & }; :', '>:']
    for dangerous in dangerous_commands:
        if dangerous in command:
            logging.warning(f"Detected potentially dangerous command: {command}")
            return False
    return True

def process_query(query, args):
    command = get_command_from_gpt(query)
    print(f"\nGenerated Command:\n{command}")

    if args.explain:
        explanation = get_explanation_from_gpt(command)
        print(f"\nExplanation:\n{explanation}")

    if args.run:
        if not is_command_safe(command):
            print("Warning: The command may be dangerous. Execution cancelled.")
            return
        confirm = input("\nDo you want to execute this command? (y/n): ")
        if confirm.lower() == 'y':
            try:
                logging.info(f"Executing command: {command}")
                result = subprocess.run(command, shell=True, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print(result.stdout)
                logging.info(f"Command executed successfully: {command}\nOutput: {result.stdout}")
            except subprocess.CalledProcessError as e:
                print(f"An error occurred while executing the command: {e.stderr}")
                logging.error(f"Command execution failed: {command}\nError: {e.stderr}")
            except KeyboardInterrupt:
                print("\nCommand execution interrupted by user.")
                logging.error(f"Command execution interrupted by user: {command}")
        else:
            print("Command execution cancelled.")
            logging.info("Command execution cancelled by user.")
    # Log the command
    logging.info(f"Query: {query}\nCommand: {command}")

def main():
    parser = argparse.ArgumentParser(description="Ask GPT for Linux command assistance.")
    parser.add_argument('-p', '--prompt', type=str, help='The prompt you want to ask GPT.')
    parser.add_argument('-r', '--run', action='store_true', help='Automatically run the command.')
    parser.add_argument('-e', '--explain', action='store_true', help='Provide an explanation of the command.')
    parser.add_argument('-i', '--interactive', action='store_true', help='Enter interactive mode.')

    args = parser.parse_args()

    if args.interactive:
        try:
            while True:
                query = input("askgpt> ")
                if query.lower() in ['exit', 'quit']:
                    break
                process_query(query, args)
        except KeyboardInterrupt:
            print("\nExiting interactive mode.")
    else:
        if not args.prompt:
            print("Please provide a prompt using -p or --prompt.")
            sys.exit(1)
        process_query(args.prompt, args)

if __name__ == "__main__":
    main()
