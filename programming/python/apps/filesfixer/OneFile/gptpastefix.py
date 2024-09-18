import re

def replace_with_space(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Replace "Copy code", "scss", "css", and "bash" with a space
    modified_content = re.sub(r'Copy\s+code|scss|css|bash|sql|Output|php|csharp|ruby|lua|yaml|powershell|python|vbnet|makefile|csv|markdown|sh', ' ', content)
    
    with open(file_path, 'w') as file:
        file.write(modified_content)

# Ask for file path
file_path = input("Enter the path of the file: ")
replace_with_space(file_path)
