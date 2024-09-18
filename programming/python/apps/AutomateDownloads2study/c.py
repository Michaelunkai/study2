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

        target_folders = []

        if "vscode" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "coding", "vscode")
            if any(tool in file_name for tool in ["extension", "plugin", "theme"]):
                tool_name = next((tool for tool in ["extension", "plugin", "theme"] if tool in file_name), "")
                target_folder = os.path.join(target_folder, tool_name)
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "claude" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "claude")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "gemini" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "gemini")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if any(keyword in file_name for keyword in ["openai", "chatgpt", "gpt"]):
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "openai")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "canva" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "documents", "canva")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if any(model in file_name for model in ["blackboxai", "anthropic", "openai", "cohere", "deepmind", "gemma", "groq", "phind", "codegemma", "mistral", "phi3", "codelama"]):
            model_name = next((model for model in ["blackboxai", "anthropic", "openai", "cohere", "deepmind", "gemma", "groq", "phind", "codegemma", "mistral", "phi3", "codelama"] if model in file_name), "")
            if model_name in ["gemma", "codegemma", "mistral", "phi3", "codelama"]:
                target_folder = os.path.join(study_path, "Artificial_Intelligence", "models", model_name.capitalize())
            else:
                target_folder = os.path.join(study_path, "Artificial_Intelligence", "models", model_name)
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)
            if model_name == "codegemma":
                additional_folder = os.path.join(study_path, "Artificial_Intelligence", "models", "CodeGemma")
                os.makedirs(additional_folder, exist_ok=True)
                target_folders.append(additional_folder)

        if "perplexity" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "chatbots", "Perplexity")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "python" in file_name or any(tool in file_name for tool in ["venv", "pip", "conda"]):
            target_folder = os.path.join(study_path, "programming", "python", "basics")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if any(keyword in file_name for keyword in ["ssh", "sshfs"]):
            target_folder = os.path.join(study_path, "ssh")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "cabina" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "image", "cabina")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "websim" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "business", "finance", "WebsimAI")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "humata" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "documents", "Humanta")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "llama" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "llama")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "phi3" in file_name or "phi-3" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "models", "phi3")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        for folder in target_folders:
            shutil.copy2(os.path.join(downloads_path, file), folder)
            copied_files[folder].append(file)

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
