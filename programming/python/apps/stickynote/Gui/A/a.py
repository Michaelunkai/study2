import os
import shutil
from collections import defaultdict

def get_all_files(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def get_all_folders(directory):
    folders = []
    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            folders.append(os.path.join(root, dir))
    return folders

def find_related_folder(file_name, folders):
    file_words = set(file_name.lower().replace('.', ' ').split())
    best_match = None
    best_score = 0
    
    for folder in folders:
        folder_name = os.path.basename(folder)
        folder_words = set(folder_name.lower().split())
        score = len(file_words.intersection(folder_words))
        if score > best_score:
            best_score = score
            best_match = folder
    
    return best_match if best_score > 0 else None

def suggest_folder_name(file_name):
    words = file_name.lower().replace('.', ' ').split()
    return '_'.join(words[:3])  # Use first 3 words of the file name

def organize_files(downloads_path, study_path):
    files = get_all_files(downloads_path)
    folders = get_all_folders(study_path)
    
    copied_files = defaultdict(list)
    suggestions = {}
    
    for file in files:
        related_folder = find_related_folder(file, folders)
        if related_folder:
            shutil.copy2(os.path.join(downloads_path, file), related_folder)
            copied_files[related_folder].append(file)
        else:
            suggested_folder = suggest_folder_name(file)
            suggestions[file] = os.path.join(study_path, suggested_folder)
    
    return copied_files, suggestions

def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"Deleted: {file_path}")
    except Exception as e:
        print(f"Error deleting {file_path}: {e}")

# Paths
downloads_path = r"C:\Users\micha\Downloads"
study_path = r"C:\study"

# Organize files
copied_files, suggestions = organize_files(downloads_path, study_path)

# Print results and ask for deletion
print("Files copied:")
for folder, files in copied_files.items():
    print(f"\nTo {folder}:")
    for file in files:
        print(f"  - {file}")
        response = input(f"Do you want to delete {file} from the downloads folder? (y/n): ").lower()
        if response == 'y':
            delete_file(os.path.join(downloads_path, file))

print("\nSuggested folders to create:")
for file, folder in suggestions.items():
    print(f"\nFor {file}:")
    print(f"  mkdir {folder}")
    print(f"  copy \"{os.path.join(downloads_path, file)}\" \"{folder}\"") 