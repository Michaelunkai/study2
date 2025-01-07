import os
from send2trash import send2trash

def delete_empty_folders(path):
    # Traverse the directory tree
    for root, dirs, files in os.walk(path, topdown=False):
        # Iterate over directories
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            try:
                # Check if directory is empty
                if not os.listdir(dir_path):
                    send2trash(dir_path)
                    print(f"Moved empty folder to recycle bin: {dir_path}")
            except PermissionError:
                print(f"Permission denied: {dir_path}")
            except Exception as e:
                print(f"Error processing directory {dir_path}: {e}")

# Get the current path
current_path = os.getcwd()
# Delete empty folders in the current path and subdirectories
delete_empty_folders(current_path)
