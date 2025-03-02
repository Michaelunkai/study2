import os
import re

def extract_tool_names(directory):
    """
    Extracts tool names from filenames in the specified directory based on predefined patterns.
    
    Args:
        directory (str): Path to the directory containing the files.
    
    Returns:
        list: Sorted list of unique tool names found.
    """
    # Define action verbs and prepositions
    action_verbs = {'setup', 'install', 'run', 'start', 'stop', 'enable', 'disable', 'configure', 'build', 'clone', 'update', 'create', 'delete'}
    prepositions = {'with', 'in', 'for', 'and', 'to', 'using', 'via', 'by', 'of'}
    
    # Initialize a set to hold unique tool names
    tools_found = set()
    
    # Check if the directory exists
    if not os.path.isdir(directory):
        print(f"Directory '{directory}' does not exist.")
        return []
    
    # Iterate over each file in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        # Skip directories
        if os.path.isdir(file_path):
            continue
        
        # Remove the file extension
        name, ext = os.path.splitext(filename)
        
        # Replace non-alphanumeric characters with spaces
        cleaned_name = re.sub(r'[^A-Za-z0-9]', ' ', name)
        
        # Split into words
        words = cleaned_name.split()
        
        # Iterate through words to find action verbs and extract tool names
        i = 0
        while i < len(words):
            word = words[i].lower()
            if word in action_verbs:
                # Start collecting tool name words
                tool_words = []
                i += 1
                while i < len(words):
                    next_word = words[i].lower()
                    if next_word in prepositions or next_word in action_verbs:
                        break
                    tool_words.append(words[i])
                    i += 1
                if tool_words:
                    # Join the tool words and normalize
                    tool_name = ' '.join(tool_words)
                    # Remove trailing numbers or underscores
                    tool_name = re.sub(r'[\d_]+$', '', tool_name)
                    # Capitalize each word in the tool name
                    tool_name = tool_name.title()
                    tools_found.add(tool_name)
            else:
                i += 1
    
    # Convert the set to a sorted list
    tool_list = sorted(tools_found)
    return tool_list

def main():
    # Define the directory containing the files
    directory = '/mnt/c/study/automation/oneliners'
    
    # Extract tools
    tools = extract_tool_names(directory)
    
    if not tools:
        print("No known tools found in the specified directory.")
        return
    
    # Print the tools as a numbered list
    for idx, tool in enumerate(tools, start=1):
        print(f"{idx}. {tool}")

if __name__ == "__main__":
    main()
