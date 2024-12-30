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
            target_folder = os.path.join(study_path, "documents", "canva")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if any(model in file_name for model in ["blackboxai", "anthropic", "openai", "cohere", "deepmind", "gemma", "groq", "phind", "codegemma", "mistral", "phi3", "codelama", "aya"]):
            model_name = next((model for model in ["blackboxai", "anthropic", "openai", "cohere", "deepmind", "gemma", "groq", "phind", "codegemma", "mistral", "phi3", "codelama", "aya"] if model in file_name), "")
            if model_name in ["gemma", "codegemma", "mistral", "phi3", "codelama", "aya"]:
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

        if "llama" in file_name or "llama" in file_name.replace("l", "1").replace("i", "l"):
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "llama")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "phi3" in file_name or "phi-3" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "models", "phi3")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "flux" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "image", "Flux")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "ai coding" in file_name or "ai_coding" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "coding")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "qnap" in file_name:
            target_folder = os.path.join(study_path, "hosting", "nas", "qnap")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "analysis" in file_name:
            target_folder = os.path.join(study_path, "security", "Analysis")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)
            additional_folder = os.path.join(study_path, "datascience", "Analytics")
            os.makedirs(additional_folder, exist_ok=True)
            target_folders.append(additional_folder)

        if "js" in file_name or "javascript" in file_name:
            target_folder = os.path.join(study_path, "programming", "frontend", "javascript", "js")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "diffusion" in file_name or "ddim" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "models", "Diffusion")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "package_manager" in file_name or "package manager" in file_name:
            target_folder = os.path.join(study_path, "linux", "Package_Manager")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "zapier" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "nocode", "zapier")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "prompt" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "prompts")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "nlp" in file_name:
            target_folder = os.path.join(study_path, "Machine_Learning", "nlp")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "flowwise" in file_name or "flowise" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "Workflow", "Flowise")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "leonardo" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "Image", "Leonardo")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "ooba" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "General", "Ooba_AI")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "gtp4all" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "OpenAI", "GPT4All")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "ai browser" in file_name or "ai_browser" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "browser_extentions")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "seo plugin" in file_name or "seo_plugin" in file_name or "seo_app_plugin" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "buisness", "marketing", "SEO.app")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "yoodli" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "Audio", "Yoodli")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "rag" in file_name:
            target_folder = os.path.join(study_path, "Machine_Learning", "rag")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "lm_studio" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "Models", "lm_studio")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "txtai" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "Data_analysis", "txtai")
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

for folder, files in copied_files.items():
    for file in files:
        response = input(f"Do you want to delete {file} from the downloads folder? (y/n): ").lower()
        if response == 'y':
            delete_file(os.path.join(downloads_path, file))