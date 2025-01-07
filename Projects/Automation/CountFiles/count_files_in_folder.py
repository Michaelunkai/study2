# count_files.py
import os

def count_files_in_directory():
    # Ask the user for a directory path
    path = input("Please enter the directory path: ")
    
    # Check if the provided path is a valid directory
    if not os.path.isdir(path):
        print("Invalid directory path")
        return
    
    # Count the number of files in the directory
    file_count = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
    
    # Print the file count
    print(f"{file_count}")

# Run the function
count_files_in_directory()
