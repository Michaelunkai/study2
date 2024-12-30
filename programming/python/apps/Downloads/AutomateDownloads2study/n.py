import os
import shutil
from collections import defaultdict

def get_all_files(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def organize_files(downloads_path, study_path):
    files = get_all_files(downloads_path)
    copied_files = defaultdict(list)

    print(f"Processing {len(files)} files")

    for file in files:
        file_name = file.lower()
        print(f"Processing file: {file}")

        target_folders = []
    if "Noisee" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\Audio\Music\Noisee"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Suno" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\Audio\Music\Suno"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Udio" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\Audio\Music\Udio"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Puzzle" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\Buisness\CustomerService\Puzzle"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Magical" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\Buisness\Marketing\Magical"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "SEO.app" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\Buisness\Marketing\SEO.app"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "WebsimAI" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\Buisness\finance\WebsimAI"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Psychologist" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\Chatbots\Character.ai\Psychologist"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Kite" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\Coding\VScode\Kite"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Pythagora" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\Coding\VScode\Pythagora"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "TabNine" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\Coding\VScode\TabNine"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "codeGPT" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\Coding\VScode\codeGPT"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "codebuddy" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\Coding\VScode\codebuddy"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "codium" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\Coding\VScode\codium"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "cody" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\Coding\VScode\cody"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "continue.dev" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\Coding\VScode\continue.dev"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "extension" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\Coding\VScode\extension"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "DataRobot" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\NoCode\Machine_learning\DataRobot"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "H2O.ai" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\NoCode\Machine_learning\H2O.ai"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Runway" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\NoCode\Machine_learning\Runway"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "TarAI" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\NoCode\Machine_learning\TarAI"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "WebsimAI" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\business\finance\WebsimAI"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Beautiful.ai" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\documents\Presentation\Beautiful.ai"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Pitch" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\documents\Presentation\Pitch"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Plus_AI" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\documents\Presentation\Plus_AI"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "SlideSpeak" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\documents\Presentation\SlideSpeak"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Tome" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\documents\Presentation\Tome"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Wepik" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\documents\Presentation\Wepik"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "gamma" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\documents\Presentation\gamma"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "gemini_api_by_google" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\gemini\gemini_api_by_google"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "llama3.1" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\llama\llama3.1"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Keras" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\neural_networks\Keras"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "bdist.linux-x86_64" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\text2speach\epub2tts\build\bdist.linux-x86_64"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "lib" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\text2speach\epub2tts\build\lib"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "epub2tts.egg-info" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\text2speach\epub2tts\epub2tts.egg-info"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "utils" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\text2speach\epub2tts\utils"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)


    if "Compose" in file_name:
        target_folder = r"C:\study\docker\Compose"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Containers" in file_name:
        target_folder = r"C:\study\docker\Containers"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Images" in file_name:
        target_folder = r"C:\study\docker\Images"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Networking" in file_name:
        target_folder = r"C:\study\docker\Networking"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Volumes" in file_name:
        target_folder = r"C:\study\docker\Volumes"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Kafka" in file_name:
        target_folder = r"C:\study\distributed_messaging\Kafka"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "RabbitMQ" in file_name:
        target_folder = r"C:\study\distributed_messaging\RabbitMQ"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Redis" in file_name:
        target_folder = r"C:\study\distributed_messaging\Redis"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "ZeroMQ" in file_name:
        target_folder = r"C:\study\distributed_messaging\ZeroMQ"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Jupyter" in file_name:
        target_folder = r"C:\study\datascience\Jupyter"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Pandas" in file_name:
        target_folder = r"C:\study\datascience\Pandas"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Spark" in file_name:
        target_folder = r"C:\study\datascience\Spark"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Tableau" in file_name:
        target_folder = r"C:\study\datascience\Tableau"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "numpy" in file_name:
        target_folder = r"C:\study\datascience\numpy"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Markdown" in file_name:
        target_folder = r"C:\study\documents\Markdown"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "PDF" in file_name:
        target_folder = r"C:\study\documents\PDF"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "CompTIA" in file_name:
        target_folder = r"C:\study\exams\CompTIA"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Fortinet" in file_name:
        target_folder = r"C:\study\firewall\Fortinet"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Palo_Alto" in file_name:
        target_folder = r"C:\study\firewall\Palo_Alto"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Sophos" in file_name:
        target_folder = r"C:\study\firewall\Sophos"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "pfsense" in file_name:
        target_folder = r"C:\study\firewall\pfsense"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Ticketing" in file_name:
        target_folder = r"C:\study\helpdesk\Ticketing"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Cloudflare" in file_name:
        target_folder = r"C:\study\hosting\Cloudflare"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Heroku" in file_name:
        target_folder = r"C:\study\hosting\Heroku"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Netlify" in file_name:
        target_folder = r"C:\study\hosting\Netlify"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Vercel" in file_name:
        target_folder = r"C:\study\hosting\Vercel"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "AKS" in file_name:
        target_folder = r"C:\study\kubernetes\AKS"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "EKS" in file_name:
        target_folder = r"C:\study\kubernetes\EKS"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "GKE" in file_name:
        target_folder = r"C:\study\kubernetes\GKE"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Helm" in file_name:
        target_folder = r"C:\study\kubernetes\Helm"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Minikube" in file_name:
        target_folder = r"C:\study\kubernetes\Minikube"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Arch" in file_name:
        target_folder = r"C:\study\linux\Arch"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "CentOS" in file_name:
        target_folder = r"C:\study\linux\CentOS"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Debian" in file_name:
        target_folder = r"C:\study\linux\Debian"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Fedora" in file_name:
        target_folder = r"C:\study\linux\Fedora"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Kali" in file_name:
        target_folder = r"C:\study\linux\Kali"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "RedHat" in file_name:
        target_folder = r"C:\study\linux\RedHat"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Ubuntu" in file_name:
        target_folder = r"C:\study\linux\Ubuntu"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "API_Gateway" in file_name:
        target_folder = r"C:\study\microservices\API_Gateway"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Service_Discovery" in file_name:
        target_folder = r"C:\study\microservices\Service_Discovery"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Service_Mesh" in file_name:
        target_folder = r"C:\study\microservices\Service_Mesh"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Grafana" in file_name:
        target_folder = r"C:\study\monitoring\Grafana"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Nagios" in file_name:
        target_folder = r"C:\study\monitoring\Nagios"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Prometheus" in file_name:
        target_folder = r"C:\study\monitoring\Prometheus"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Zabbix" in file_name:
        target_folder = r"C:\study\monitoring\Zabbix"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Grafana" in file_name:
        target_folder = r"C:\study\monitoring\Grafana"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Nagios" in file_name:
        target_folder = r"C:\study\monitoring\Nagios"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Prometheus" in file_name:
        target_folder = r"C:\study\monitoring\Prometheus"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Zabbix" in file_name:
        target_folder = r"C:\study\monitoring\Zabbix"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "C" in file_name:
        target_folder = r"C:\study\programming\C"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "C++" in file_name:
        target_folder = r"C:\study\programming\C++"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Go" in file_name:
        target_folder = r"C:\study\programming\Go"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Java" in file_name:
        target_folder = r"C:\study\programming\Java"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "JavaScript" in file_name:
        target_folder = r"C:\study\programming\JavaScript"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Python" in file_name:
        target_folder = r"C:\study\programming\Python"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Ruby" in file_name:
        target_folder = r"C:\study\programming\Ruby"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Rust" in file_name:
        target_folder = r"C:\study\programming\Rust"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Encryption" in file_name:
        target_folder = r"C:\study\security\Encryption"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Penetration_Testing" in file_name:
        target_folder = r"C:\study\security\Penetration_Testing"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Vulnerability_Scanning" in file_name:
        target_folder = r"C:\study\security\Vulnerability_Scanning"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Burp_Suite" in file_name:
        target_folder = r"C:\study\security\Burp_Suite"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Metasploit" in file_name:
        target_folder = r"C:\study\security\Metasploit"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Nmap" in file_name:
        target_folder = r"C:\study\security\Nmap"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Wireshark" in file_name:
        target_folder = r"C:\study\security\Wireshark"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)
    if "Arch" in file_name:
        target_folder = r"C:\study\setups\Arch"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Debian" in file_name:
        target_folder = r"C:\study\setups\Debian"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Fedora" in file_name:
        target_folder = r"C:\study\setups\Fedora"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Ubuntu" in file_name:
        target_folder = r"C:\study\setups\Ubuntu"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)
    if "Keys" in file_name:
        target_folder = r"C:\study\ssh\Keys"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Tunneling" in file_name:
        target_folder = r"C:\study\ssh\Tunneling"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Networking" in file_name:
        target_folder = r"C:\study\troubleshooting\Networking"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "System" in file_name:
        target_folder = r"C:\study\troubleshooting\System"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Hyper-V" in file_name:
        target_folder = r"C:\study\virtualmachines\Hyper-V"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "KVM" in file_name:
        target_folder = r"C:\study\virtualmachines\KVM"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "VirtualBox" in file_name:
        target_folder = r"C:\study\virtualmachines\VirtualBox"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "VMware" in file_name:
        target_folder = r"C:\study\virtualmachines\VMware"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Active_Directory" in file_name:
        target_folder = r"C:\study\windows\Active_Directory"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Group_Policy" in file_name:
        target_folder = r"C:\study\windows\Group_Policy"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "PowerShell" in file_name:
        target_folder = r"C:\study\windows\PowerShell"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Registry" in file_name:
        target_folder = r"C:\study\windows\Registry"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "GCP" in file_name:
        target_folder = r"C:\study\cloud\GCP"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Hybrid" in file_name:
        target_folder = r"C:\study\cloud\Hybrid"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "IBM" in file_name:
        target_folder = r"C:\study\cloud\IBM"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "IaaS" in file_name:
        target_folder = r"C:\study\cloud\IaaS"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Koyeb" in file_name:
        target_folder = r"C:\study\cloud\Koyeb"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Labs" in file_name:
        target_folder = r"C:\study\cloud\Labs"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "PaaS" in file_name:
        target_folder = r"C:\study\cloud\PaaS"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "SaaS" in file_name:
        target_folder = r"C:\study\cloud\SaaS"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "aws" in file_name:
        target_folder = r"C:\study\cloud\aws"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "azure" in file_name:
        target_folder = r"C:\study\cloud\azure"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "cloud_foundry" in file_name:
        target_folder = r"C:\study\cloud\cloud_foundry"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "filecloud" in file_name:
        target_folder = r"C:\study\cloud\filecloud"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "owncloud" in file_name:
        target_folder = r"C:\study\cloud\owncloud"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "serverless" in file_name:
        target_folder = r"C:\study\cloud\serverless"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Basics" in file_name:
        target_folder = r"C:\study\cluster\Basics"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Ceph" in file_name:
        target_folder = r"C:\study\cluster\Ceph"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Cloud" in file_name:
        target_folder = r"C:\study\cluster\Cloud"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Clustering_with_K-Means" in file_name:
        target_folder = r"C:\study\cluster\Clustering_with_K-Means"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "CockRoachDB" in file_name:
        target_folder = r"C:\study\cluster\CockRoachDB"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Databases" in file_name:
        target_folder = r"C:\study\cluster\Databases"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "DockerSwarm" in file_name:
        target_folder = r"C:\study\cluster\DockerSwarm"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "EKS" in file_name:
        target_folder = r"C:\study\cluster\EKS"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Minikube" in file_name:
        target_folder = r"C:\study\cluster\Minikube"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "kmeans" in file_name:
        target_folder = r"C:\study\cluster\kmeans"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "kubernetes" in file_name:
        target_folder = r"C:\study\cluster\kubernetes"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "prestodb" in file_name:
        target_folder = r"C:\study\cluster\prestodb"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "proxmox" in file_name:
        target_folder = r"C:\study\cluster\proxmox"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "redshift" in file_name:
        target_folder = r"C:\study\cluster\redshift"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Jami" in file_name:
        target_folder = r"C:\study\communication\Jami"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "MessageBird" in file_name:
        target_folder = r"C:\study\communication\MessageBird"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Vonage" in file_name:
        target_folder = r"C:\study\communication\Vonage"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "bandwidtch" in file_name:
        target_folder = r"C:\study\communication\bandwidtch"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "ferdium" in file_name:
        target_folder = r"C:\study\communication\ferdium"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "hexchat" in file_name:
        target_folder = r"C:\study\communication\hexchat"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "linphone" in file_name:
        target_folder = r"C:\study\communication\linphone"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "pilvo" in file_name:
        target_folder = r"C:\study\communication\pilvo"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "qTox" in file_name:
        target_folder = r"C:\study\communication\qTox"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "revolt" in file_name:
        target_folder = r"C:\study\communication\revolt"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "sinch" in file_name:
        target_folder = r"C:\study\communication\sinch"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "telnyx" in file_name:
        target_folder = r"C:\study\communication\telnyx"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "twillio" in file_name:
        target_folder = r"C:\study\communication\twillio"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)


    if "Monero" in file_name:
        target_folder = r"C:\study\blockchain\Monero"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "solana" in file_name:
        target_folder = r"C:\study\blockchain\solana"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "rsync" in file_name:
        target_folder = r"C:\study\backup\rsync"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Airflow" in file_name:
        target_folder = r"C:\study\automation\Airflow"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "CI-CD" in file_name:
        target_folder = r"C:\study\automation\CI-CD"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Data_Processing" in file_name:
        target_folder = r"C:\study\automation\Data_Processing"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Dorkbot" in file_name:
        target_folder = r"C:\study\automation\Dorkbot"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Earthly" in file_name:
        target_folder = r"C:\study\automation\Earthly"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "HashiCorp" in file_name:
        target_folder = r"C:\study\automation\HashiCorp"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Infrastructure_as_Code" in file_name:
        target_folder = r"C:\study\automation\Infrastructure_as_Code"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Internal" in file_name:
        target_folder = r"C:\study\automation\Internal"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "JUnit" in file_name:
        target_folder = r"C:\study\automation\JUnit"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Packer" in file_name:
        target_folder = r"C:\study\automation\Packer"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "cron" in file_name:
        target_folder = r"C:\study\automation\cron"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "home_assistant" in file_name:
        target_folder = r"C:\study\automation\home_assistant"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "oneliners" in file_name:
        target_folder = r"C:\study\automation\oneliners"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "sync" in file_name:
        target_folder = r"C:\study\automation\sync"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "updates" in file_name:
        target_folder = r"C:\study\automation\updates"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "CodeCommit" in file_name:
        target_folder = r"C:\study\Version_control\CodeCommit"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "GithubPages" in file_name:
        target_folder = r"C:\study\Version_control\GithubPages"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "flyway" in file_name:
        target_folder = r"C:\study\Version_control\flyway"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "git" in file_name:
        target_folder = r"C:\study\Version_control\git"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "gitea" in file_name:
        target_folder = r"C:\study\Version_control\gitea"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "github" in file_name:
        target_folder = r"C:\study\Version_control\github"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "gitlab" in file_name:
        target_folder = r"C:\study\Version_control\gitlab"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "labeler" in file_name:
        target_folder = r"C:\study\Version_control\labeler"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Allure" in file_name:
        target_folder = r"C:\study\Testing\Allure"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Behat" in file_name:
        target_folder = r"C:\study\Testing\Behat"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Bugzilla" in file_name:
        target_folder = r"C:\study\Testing\Bugzilla"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Cucumber" in file_name:
        target_folder = r"C:\study\Testing\Cucumber"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "JBehave" in file_name:
        target_folder = r"C:\study\Testing\JBehave"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "KatalonStudio" in file_name:
        target_folder = r"C:\study\Testing\KatalonStudio"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "PyTest" in file_name:
        target_folder = r"C:\study\Testing\PyTest"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "RSpec" in file_name:
        target_folder = r"C:\study\Testing\RSpec"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "SoapUI" in file_name:
        target_folder = r"C:\study\Testing\SoapUI"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "SonarQube" in file_name:
        target_folder = r"C:\study\Testing\SonarQube"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Specflow" in file_name:
        target_folder = r"C:\study\Testing\Specflow"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)


        if "bash" in file_name:
            target_folder = r"C:\study\Shells\bash"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

    if "powershell" in file_name:
        target_folder = r"C:\study\Shells\powershell"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "zsh" in file_name:
        target_folder = r"C:\study\Shells\zsh"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)


    if "Cuda" in file_name:
        target_folder = r"C:\study\Nvidia\Cuda"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Nvidia_Local_AI" in file_name:
        target_folder = r"C:\study\Nvidia\Nvidia_Local_AI"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Cloud" in file_name:
        target_folder = r"C:\study\Machine_Learning\Cloud"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Clustering_with_K-Means" in file_name:
        target_folder = r"C:\study\Machine_Learning\Clustering_with_K-Means"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Diffusion" in file_name:
        target_folder = r"C:\study\Machine_Learning\Diffusion"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Gamify" in file_name:
        target_folder = r"C:\study\Machine_Learning\Gamify"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "GoogleColab" in file_name:
        target_folder = r"C:\study\Machine_Learning\GoogleColab"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "LLM" in file_name:
        target_folder = r"C:\study\Machine_Learning\LLM"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Model_Training" in file_name:
        target_folder = r"C:\study\Machine_Learning\Model_Training"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Modeling" in file_name:
        target_folder = r"C:\study\Machine_Learning\Modeling"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "NLP" in file_name:
        target_folder = r"C:\study\Machine_Learning\NLP"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Neural_Networks" in file_name:
        target_folder = r"C:\study\Machine_Learning\Neural_Networks"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "RAG" in file_name:
        target_folder = r"C:\study\Machine_Learning\RAG"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Upscaler" in file_name:
        target_folder = r"C:\study\Machine_Learning\Upscaler"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "edge_computing" in file_name:
        target_folder = r"C:\study\Machine_Learning\edge_computing"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "forests" in file_name:
        target_folder = r"C:\study\Machine_Learning\forests"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "projects" in file_name:
        target_folder = r"C:\study\Machine_Learning\projects"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "tuning" in file_name:
        target_folder = r"C:\study\Machine_Learning\tuning"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)


    if "Intrusion_Detection" in file_name:
        target_folder = r"C:\study\Hacking\Intrusion_Detection"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "ManInTheMiddle" in file_name:
        target_folder = r"C:\study\Hacking\ManInTheMiddle"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "OSINT" in file_name:
        target_folder = r"C:\study\Hacking\OSINT"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Search_Engines" in file_name:
        target_folder = r"C:\study\Hacking\Search_Engines"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "botnet" in file_name:
        target_folder = r"C:\study\Hacking\botnet"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "ddos-dos" in file_name:
        target_folder = r"C:\study\Hacking\ddos-dos"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "exploits" in file_name:
        target_folder = r"C:\study\Hacking\exploits"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "flaws.clowd" in file_name:
        target_folder = r"C:\study\Hacking\flaws.clowd"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "info_gathering" in file_name:
        target_folder = r"C:\study\Hacking\info_gathering"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "malware" in file_name:
        target_folder = r"C:\study\Hacking\malware"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "overthewire" in file_name:
        target_folder = r"C:\study\Hacking\overthewire"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "passwordCracking" in file_name:
        target_folder = r"C:\study\Hacking\passwordCracking"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "payloads" in file_name:
        target_folder = r"C:\study\Hacking\payloads"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "pentesting" in file_name:
        target_folder = r"C:\study\Hacking\pentesting"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "phishing" in file_name:
        target_folder = r"C:\study\Hacking\phishing"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "privilege_escalation" in file_name:
        target_folder = r"C:\study\Hacking\privilege_escalation"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "reverseSHELL" in file_name:
        target_folder = r"C:\study\Hacking\reverseSHELL"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "spoofing" in file_name:
        target_folder = r"C:\study\Hacking\spoofing"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "vulnerabilty" in file_name:
        target_folder = r"C:\study\Hacking\vulnerabilty"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "wireshark" in file_name:
        target_folder = r"C:\study\Hacking\wireshark"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)


    if "Convolutional_Layers" in file_name:
        target_folder = r"C:\study\DeepLearning\Convolutional_Layers"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "DeepNetworks" in file_name:
        target_folder = r"C:\study\DeepLearning\DeepNetworks"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "DeepQ" in file_name:
        target_folder = r"C:\study\DeepLearning\DeepQ"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Detection" in file_name:
        target_folder = r"C:\study\DeepLearning\Detection"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "FastAI" in file_name:
        target_folder = r"C:\study\DeepLearning\FastAI"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "FrameWorks" in file_name:
        target_folder = r"C:\study\DeepLearning\FrameWorks"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "GPU" in file_name:
        target_folder = r"C:\study\DeepLearning\GPU"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Proximal_Policy" in file_name:
        target_folder = r"C:\study\DeepLearning\Proximal_Policy"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "SRCNN" in file_name:
        target_folder = r"C:\study\DeepLearning\SRCNN"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Unity" in file_name:
        target_folder = r"C:\study\DeepLearning\Unity"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "VS" in file_name:
        target_folder = r"C:\study\DeepLearning\VS"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)


    if "degrees_and_length_converter" in file_name:
        target_folder = r"C:\study\Converting\degrees_and_length_converter"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Cisco_AnyConnect" in file_name:
        target_folder = r"C:\study\Cisco\Cisco_AnyConnect"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "GNS3" in file_name:
        target_folder = r"C:\study\Cisco\GNS3"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Packet_Tracer" in file_name:
        target_folder = r"C:\study\Cisco\Packet_Tracer"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)


    if "Centralized" in file_name:
        target_folder = r"C:\study\Centralized_Logging\Centralized"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "ELK" in file_name:
        target_folder = r"C:\study\Centralized_Logging\ELK"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Fluent" in file_name:
        target_folder = r"C:\study\Centralized_Logging\Fluent"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Loki" in file_name:
        target_folder = r"C:\study\Centralized_Logging\Loki"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "ZooKeeper" in file_name:
        target_folder = r"C:\study\Centralized_Logging\ZooKeeper"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "flink" in file_name:
        target_folder = r"C:\study\Centralized_Logging\flink"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "graylog" in file_name:
        target_folder = r"C:\study\Centralized_Logging\graylog"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "logz" in file_name:
        target_folder = r"C:\study\Centralized_Logging\logz"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "miniO" in file_name:
        target_folder = r"C:\study\Centralized_Logging\miniO"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "solr" in file_name:
        target_folder = r"C:\study\Centralized_Logging\solr"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "splunk" in file_name:
        target_folder = r"C:\study\Centralized_Logging\splunk"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "storm" in file_name:
        target_folder = r"C:\study\Centralized_Logging\storm"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)


    if "Agents" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\Agents"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Audio" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\Audio"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "BuildBots" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\BuildBots"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Buisness" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\Buisness"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Chatbots" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\Chatbots"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Claude" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\Claude"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Coding" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\Coding"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Data_analysis" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\Data_analysis"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "General" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\General"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Image" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\Image"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Local" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\Local"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Models" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\Models"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Multiplatform" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\Multiplatform"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "NoCode" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\NoCode"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "OpenAI" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\OpenAI"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "SheetAI" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\SheetAI"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Shopping" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\Shopping"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "SocialMedia" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\SocialMedia"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Transcription" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\Transcription"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Uncensored" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\Uncensored"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Video" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\Video"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "WebBuilding" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\WebBuilding"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Workflow" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\Workflow"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Writting" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\Writting"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "browser_extentions" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\browser_extentions"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "business" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\business"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "copilot" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\copilot"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "documents" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\documents"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "gemini" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\gemini"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "llama" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\llama"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "neural_networks" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\neural_networks"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "perplexity" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\perplexity"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "prompts" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\prompts"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "text2speach" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence\text2speach"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)


    if "termux" in file_name:
        target_folder = r"C:\study\Android\termux"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Android" in file_name:
        target_folder = r"C:\study\Android"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Artificial_Intelligence" in file_name:
        target_folder = r"C:\study\Artificial_Intelligence"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Centralized_Logging" in file_name:
        target_folder = r"C:\study\Centralized_Logging"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Cisco" in file_name:
        target_folder = r"C:\study\Cisco"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Converting" in file_name:
        target_folder = r"C:\study\Converting"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Credentials" in file_name:
        target_folder = r"C:\study\Credentials"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "DeepLearning" in file_name:
        target_folder = r"C:\study\DeepLearning"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Hacking" in file_name:
        target_folder = r"C:\study\Hacking"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Machine_Learning" in file_name:
        target_folder = r"C:\study\Machine_Learning"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Nvidia" in file_name:
        target_folder = r"C:\study\Nvidia"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Shells" in file_name:
        target_folder = r"C:\study\Shells"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Testing" in file_name:
        target_folder = r"C:\study\Testing"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "Version_control" in file_name:
        target_folder = r"C:\study\Version_control"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "automation" in file_name:
        target_folder = r"C:\study\automation"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "backup" in file_name:
        target_folder = r"C:\study\backup"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "blockchain" in file_name:
        target_folder = r"C:\study\blockchain"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "cloud" in file_name:
        target_folder = r"C:\study\cloud"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "cluster" in file_name:
        target_folder = r"C:\study\cluster"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "communication" in file_name:
        target_folder = r"C:\study\communication"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "datascience" in file_name:
        target_folder = r"C:\study\datascience"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "distributed_messaging" in file_name:
        target_folder = r"C:\study\distributed_messaging"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "docker" in file_name:
        target_folder = r"C:\study\docker"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "documents" in file_name:
        target_folder = r"C:\study\documents"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "exams" in file_name:
        target_folder = r"C:\study\exams"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "firewall" in file_name:
        target_folder = r"C:\study\firewall"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "helpdesk" in file_name:
        target_folder = r"C:\study\helpdesk"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "hosting" in file_name:
        target_folder = r"C:\study\hosting"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "kubernetes" in file_name:
        target_folder = r"C:\study\kubernetes"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "linux" in file_name:
        target_folder = r"C:\study\linux"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "microservices" in file_name:
        target_folder = r"C:\study\microservices"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "monitoring" in file_name:
        target_folder = r"C:\study\monitoring"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "networking" in file_name:
        target_folder = r"C:\study\networking"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "programming" in file_name:
        target_folder = r"C:\study\programming"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "security" in file_name:
        target_folder = r"C:\study\security"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "setups" in file_name:
        target_folder = r"C:\study\setups"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "ssh" in file_name:
        target_folder = r"C:\study\ssh"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "troubleshooting" in file_name:
        target_folder = r"C:\study\troubleshooting"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "virtualmachines" in file_name:
        target_folder = r"C:\study\virtualmachines"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)

    if "windows" in file_name:
        target_folder = r"C:\study\windows"
        os.makedirs(target_folder, exist_ok=True)
        target_folders.append(target_folder)


        if "Intrusion_Detection" in file_name:
            target_folder = r"C:\study\hacking\Intrusion_Detection"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "flaws.clowd" in file_name:
            target_folder = r"C:\study\hacking\flaws.clowd"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "phishing" in file_name:
            target_folder = r"C:\study\hacking\phishing"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "ManInTheMiddle" in file_name:
            target_folder = r"C:\study\hacking\ManInTheMiddle"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "info_gathering" in file_name:
            target_folder = r"C:\study\hacking\info_gathering"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "privilege_escalation" in file_name:
            target_folder = r"C:\study\hacking\privilege_escalation"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "OSINT" in file_name:
            target_folder = r"C:\study\hacking\OSINT"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "malware" in file_name:
            target_folder = r"C:\study\hacking\malware"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "reverseSHELL" in file_name:
            target_folder = r"C:\study\hacking\reverseSHELL"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "Search_Engines" in file_name:
            target_folder = r"C:\study\hacking\Search_Engines"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "overthewire" in file_name:
            target_folder = r"C:\study\hacking\overthewire"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "spoofing" in file_name:
            target_folder = r"C:\study\hacking\spoofing"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "botnet" in file_name:
            target_folder = r"C:\study\hacking\botnet"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "passwordCracking" in file_name:
            target_folder = r"C:\study\hacking\passwordCracking"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "vulnerabilty" in file_name:
            target_folder = r"C:\study\hacking\vulnerabilty"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "ddos-dos" in file_name:
            target_folder = r"C:\study\hacking\ddos-dos"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "payloads" in file_name:
            target_folder = r"C:\study\hacking\payloads"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "wireshark" in file_name:
            target_folder = r"C:\study\hacking\wireshark"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "exploits" in file_name:
                target_folder = r"C:\study\hacking\exploits"
                os.makedirs(target_folder, exist_ok=True)
                target_folders.append(target_folder)

        if "pentesting" in file_name:
            target_folder = r"C:\study\hacking\pentesting"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)


        if "monitor" in file_name or "monitoring" in file_name:
            target_folder = r"C:\study\monitoring"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "snort" in file_name:
            target_folder = r"C:\study\hacking\Intrusion_Detection\snort"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "splunk" in file_name:
            target_folder = r"C:\study\Centralized_Logging\splunk"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "phind" in file_name:
            target_folder = os.path.join(study_path, "Artificial_Intelligence", "Multiplatform", "Phind")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "codeguru" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "codeguru")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws awstats" in file_name or "aws_awstats" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "AWStats")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws awstats" in file_name or "aws_awstats" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "AWStats")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws ce" in file_name or "aws_ce" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "CE")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws cloudfront" in file_name or "aws_cloudfront" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "CloudFront")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws codepipeline" in file_name or "aws_codepipeline" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "CodePipeLine")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws dynamodb" in file_name or "aws_dynamodb" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "DynamoDB")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws ebs" in file_name or "aws_ebs" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "EBS")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws ec2" in file_name or "aws_ec2" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "EC2")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws ecs" in file_name or "aws_ecs" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "ECS")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws efs" in file_name or "aws_efs" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "EFS")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws eks" in file_name or "aws_eks" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "EKS")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws elb" in file_name or "aws_elb" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "ELB")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws elbv2" in file_name or "aws_elbv2" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "ELBv2")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws emr" in file_name or "aws_emr" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "EMR")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws iam" in file_name or "aws_iam" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "IAM")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws kms" in file_name or "aws_kms" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "KMS")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws kinesis" in file_name or "aws_kinesis" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "Kinesis")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws polly" in file_name or "aws_polly" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "Polly")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws rds" in file_name or "aws_rds" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "RDS")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws redshift" in file_name or "aws_redshift" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "Redshift")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws rekognition" in file_name or "aws_rekognition" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "Rekognition")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws route53" in file_name or "aws_route53" in file_name:
           target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "Route53")
           os.makedirs(target_folder, exist_ok=True)
           target_folders.append(target_folder)

        if "aws sam" in file_name or "aws_sam" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "SAM")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws sns" in file_name or "aws_sns" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "SNS")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws sqs" in file_name or "aws_sqs" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "SQS")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws sagemaker" in file_name or "aws_sagemaker" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "SageMaker")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws secretsmanager" in file_name or "aws_secretsmanager" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "SecretsManager")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws x-ray" in file_name or "aws_x-ray" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "X-ray")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws amplify" in file_name or "aws_amplify" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "amplify")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws apigateway" in file_name or "aws_apigateway" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "apigateway")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws boto3" in file_name or "aws_boto3" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "boto3")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws cloudformation" in file_name or "aws_cloudformation" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "cloudformation")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws cloudwatch" in file_name or "aws_cloudwatch" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "cloudwatch")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws comprehend" in file_name or "aws_comprehend" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "comprehend")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws elasticbeanstalk" in file_name or "aws_elasticbeanstalk" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "elasticbeanstalk")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws general" in file_name or "aws_general" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "general")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws glue" in file_name or "aws_glue" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "glue")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws lambda" in file_name or "aws_lambda" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "lambda")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws iot" in file_name or "aws_iot" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "loT")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws proton" in file_name or "aws_proton" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "proton")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws sessionmanager" in file_name or "aws_sessionmanager" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "sessionManger")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws stacks" in file_name or "aws_stacks" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "stacks")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws vpc" in file_name or "aws_vpc" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "vpc")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws_s3" in file_name or "aws s3" in file_name:
            target_folder = r"C:\study\cloud\aws\awscli\s3"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "subprocess.Popen" in file_name or "subprocess_popen" in file_name:
            target_folder = r"C:\study\shells\powershell\subprocess.Popen"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "convert" in file_name or "converting" in file_name:
            target_folder = r"C:\study\Converting"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws comprehend" in file_name or "aws_comprehend" in file_name:
            target_folder = r"C:\study\cloud\aws\awscli\comprehend"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "mind map" in file_name or "mindmap" in file_name or "mind_map" in file_name:
            target_folder = r"C:\study\datascience\mindmaps"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "reverse" in file_name:
            target_folder = r"C:\study\datascience\reverse_engineering"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "github pages" in file_name or "github_pages" in file_name:
            target_folder = r"C:\study\Version_Control\GithubPages"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "colab-cli" in file_name or "colab cli" in file_name:
            target_folder = r"C:\study\Machine_Learning\googlecolab\colab-cli"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "aws ce" in file_name or "aws_ce" in file_name:
            target_folder = os.path.join(study_path, "cloud", "aws", "awscli", "CE")
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "Invoke-WebRequest" in file:
            target_folder = r"C:\study\shells\powershell\Invoke-WebRequest"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "streamlit" in file_name:
            target_folder = r"C:\study\DeepLearning\FrameWorks\UI_Makers\Streamlit"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "gradio" in file_name:
            target_folder = r"C:\study\DeepLearning\FrameWorks\UI_Makers\Gradio"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "stable diffusion" in file_name:
            target_folder = r"C:\study\Artificial_Intelligence\image\stable_diffiusion"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

        if "Get-WmiObject" in file:  # Note: not lowercased
            target_folder = r"C:\study\shells\powershell\Get-WmiObject"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)
            print(f"Matched Get-WmiObject: {file}")

        if "iwr" in file_name:
            target_folder = r"C:\study\shells\powershell\IWR"
            os.makedirs(target_folder, exist_ok=True)
            target_folders.append(target_folder)

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

        if "midjourney" in file_name:
            target_folder = r"C:\study\Artificial_Intelligence\image\MidJourney"
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
            try:
                shutil.copy2(os.path.join(downloads_path, file), folder)
                copied_files[folder].append(file)
                print(f"Copied {file} to {folder}")
            except Exception as e:
                print(f"Error copying {file} to {folder}: {e}")

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
