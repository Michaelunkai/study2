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


        if "Start-Process" in file_name or "StartProcess" in file_name or "StartProcessInstall" in file_name:
            target_folder = r"C:\study\windows\powershell\startprocess"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "choco" in file_name:
            target_folder = r"C:\study\windows\choco"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "nikto" in file_name:
            target_folder = r"C:\study\Hacking\vulnerabilty\nikto"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "nmap" in file_name:
            target_folder = r"C:\study\hacking\nmap"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "snap" in file_name:
            target_folder = r"C:\study\linux\Package_Manager\snap"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "encryption" in file_name:
            target_folder = r"C:\study\security\Encryption"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "deep learning" in file_name:
            target_folder = r"C:\study\DeepLearning"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "dall-e" in file_name or "dalle" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "image", "DALL-E")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)
            
        if "flux" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "image", "flux")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if 'algorithm' in file_name or 'algorithms' in file_name:
            target_folder = r"C:\study\datascience\algorithms"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "colab" in file_name:
            target_folder = os.path.join(study_path, "Machine_Learning", "googlecolab")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "torch" in file_name or "pytorch" in file_name:
            target_folder = os.path.join(study_path, "DeepLearning", "FrameWorks", "torch")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "tensorflow" in file_name:
            target_folder = os.path.join(study_path, "DeepLearning", "FrameWorks", "tensorflow")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if file.endswith('.ipynb'):
            target_folder = r"C:\study\programming\python\datascience\ipynb"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)


        if "lmsys" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "Multiplatform", "lmsys")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)


        if "collab" in file_name and "download" in file_name:
            target_folder = os.path.join(study_path, "Machine_Learning", "GoogleColab", "Notebooks", "Download_Notebooks")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)


        if "vagrant" in file_name:
            target_folder = os.path.join(study_path, "virtualmachines", "Vagrant")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)


        if "jenkins" in file_name:
            target_folder = os.path.join(study_path, "automation", "CI-CD", "jenkins")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)


        if "ai models" in file_name or "ai_models" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "models")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        
        if "neural network" in file_name:
            target_folder = os.path.join(study_path, "Machine_Learning", "Neural_Networks")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "restapi" in file_name:
            target_folder = os.path.join(study_path, "programming", "APIs", "restAPI")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "anthropic" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "claude")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "api" in file_name:
            target_folder = os.path.join(study_path, "programming", "APIs")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "fastfetch" in file_name:
            target_folder = os.path.join(study_path, "linux", "fastfetch")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "scrapy" in file_name:
            target_folder = os.path.join(study_path, "Hacking", "info_gathering", "Scrapy")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)


        if "clamav" in file_name:
            target_folder = os.path.join(study_path, "firewall", "clamAV")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "Get-Command" in file_name or 'Get commands' in file_name:
            target_folder = os.path.join(study_path, "windows", "powershell", "Get-Command")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)


        if "awk" in file_name:
            target_folder = os.path.join(study_path, "linux", "bash", "awk")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)


        if "fallocate" in file_name:
            target_folder = os.path.join(study_path, "linux", "fallocate")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)


        if "rsync" in file_name:
            target_folder = os.path.join(study_path, "backup", "rsync")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)


        if "notebooklm" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "documents", "NotebookLM")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        
        if "elk" in file_name:
            target_folder = os.path.join(study_path, "Centralized_Logging", "ELK")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "ceph" in file_name:
            target_folder = os.path.join(study_path, "cluster", "ceph")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)


        if "wget" in file_name:
            target_folder = os.path.join(study_path, "Hacking", "info_gathering", "Wget")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "msty" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "local", "Msty")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)


        if "winget" in file_name:
            target_folder = os.path.join(study_path, "windows", "powershell", "winget")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)


        if "autohotkey" in file_name:
            target_folder = os.path.join(study_path, "windows", "AutoHotkey")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "user management" in file_name or "user_management" in file_name:
            target_folder = os.path.join(study_path, "linux", "bash", "User_Management")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)
        
        if "transformers" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "local", "huggingface", "Transformers")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "huggingface" in file_name or "hugging face" in file_name:
            if "transformers" not in file_name:
                target_folder = os.path.join(study_path, "Artificial_Intelligence", "local", "huggingface")
                os.makedirs(target_folder, exist_ok=True)
                target_folders.append(target_folder)
        
        if "model" in file_name and "training" in file_name:
            target_folder = os.path.join(study_path, "Machine_Learning", "Model_Training")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

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

        if "jan" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "local", "jan")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "vibe" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "Audio", "VibeAI")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "osint" in file_name:
            target_folder = os.path.join(study_path, "Hacking", "OSINT")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "llm" in file_name:
            target_folder = os.path.join(study_path, "Machine_Learning", "llm")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)
            if "vllm" in file_name:
                target_folder = os.path.join(target_folder, "vllm")
                os.makedirs(target_folder, exist_ok=True)
                target_folders.append(target_folder)

        if "magical_meeting_tool_description" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "buisness", "marketing", "Magical")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "chatbot" in file_name or "chatbots" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "Chatbots")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "qwen2" in file_name or "qwen" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "models", "qwen")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "lex" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "lex")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "chatpdf" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "documents", "chatpdf")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "zebracat" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "video", "Zebracat")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "liner" in file_name:
            target_folder = os.path.join(study_path, "automation", "oneliners")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "setup" in file_name:
            target_folder = os.path.join(study_path, "setups")
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
# Print results
print("Files copied:")
for folder, files in copied_files.items():
    print(f"\nTo {folder}:")
    for file in files:
        print(f"  - {file}")

# Delete original files after copying
for folder, files in copied_files.items():
    for file in files:
        delete_file(os.path.join(downloads_path, file))
