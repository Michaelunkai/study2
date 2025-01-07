import os
import re

def replace_with_space_in_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    modified_lines = []
    for line in lines:
        # Strip the line to check for backticks only
        stripped_line = line.strip()
        
        # Check if the line contains only ```
        if stripped_line == "```":
            continue
        
        # Count the number of words in the line
        word_count = len(line.split())
        
        if word_count <= 3:
            # Replace specified words with a space
            line = re.sub(r'Copy\s+code|scss|css|bash|sql|Output|php|csharp|ruby|lua|yaml|powershell|python|vbnet|makefile|csv|markdown|sh|```|```sh', ' ', line)
        
        modified_lines.append(line)

    with open(file_path, 'w') as file:
        file.writelines(modified_lines)

def process_all_files_in_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            replace_with_space_in_file(file_path)

# Process all files in the current directory
current_directory = os.getcwd()
process_all_files_in_directory(current_directory)
