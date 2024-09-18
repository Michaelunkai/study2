import os
import shutil
from collections import defaultdict

def get_all_files(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def organize_files(downloads_path, study_path):
    files = get_all_files(downloads_path)
    
    copied_files = defaultdict(list)
    
    for file in files:
        file_name = file.lower()
        
        if "vscode" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "coding", "vscode")
            if any(tool in file_name for tool in ["extension", "plugin", "theme"]):
                tool_name = next((tool for tool in ["extension", "plugin", "theme"] if tool in file_name), "")
                target_folder = os.path.join(target_folder, tool_name)
                os.makedirs(target_folder, exist_ok=True)
            shutil.copy2(os.path.join(downloads_path, file), target_folder)
            copied_files[target_folder].append(file)
        
        elif "claude" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "claude")
            shutil.copy2(os.path.join(downloads_path, file), target_folder)
            copied_files[target_folder].append(file)
        
        elif "gemini" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "gemini")
            shutil.copy2(os.path.join(downloads_path, file), target_folder)
            copied_files[target_folder].append(file)
        
        elif any(keyword in file_name for keyword in ["openai", "chatgpt", "gpt"]):
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "openai")
            shutil.copy2(os.path.join(downloads_path, file), target_folder)
            copied_files[target_folder].append(file)
        
        elif "canva" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "documents", "canva")
            shutil.copy2(os.path.join(downloads_path, file), target_folder)
            copied_files[target_folder].append(file)
        
        elif any(model in file_name for model in ["blackboxai", "anthropic", "openai", "cohere", "deepmind"]):
            model_name = next((model for model in ["blackboxai", "anthropic", "openai", "cohere", "deepmind"] if model in file_name), "")
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "models", model_name)
            os.makedirs(target_folder, exist_ok=True)
            shutil.copy2(os.path.join(downloads_path, file), target_folder)
            copied_files[target_folder].append(file)
        
        elif "perplexity" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "chatbots", "Perplexity")
            shutil.copy2(os.path.join(downloads_path, file), target_folder)
            copied_files[target_folder].append(file)
        
        elif "python" in file_name:
            target_folder = os.path.join(study_path, "programming", "python", "basics")
            shutil.copy2(os.path.join(downloads_path, file), target_folder)
            copied_files[target_folder].append(file)
    
    return copied_files

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
copied_files = organize_files(downloads_path, study_path)

# Print results and ask for deletion
print("Files copied:")
for folder, files in copied_files.items():
    print(f"\nTo {folder}:")
    for file in files:
        print(f"  - {file}")
        response = input(f"Do you want to delete {file} from the downloads folder? (y/n): ").lower()
        if response == 'y':
            delete_file(os.path.join(downloads_path, file))
