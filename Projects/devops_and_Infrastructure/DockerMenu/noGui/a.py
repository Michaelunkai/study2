import subprocess
import sys

def run_command_as_admin(command):
    try:
        subprocess.run(command, shell=True, executable='/bin/bash', check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def get_input(prompt):
    return input(prompt).strip()

def run_selected_commands(selected_commands):
    command_to_run = " && ".join(selected_commands)
    run_command_as_admin(command_to_run)

def main():
    commands = [
        {"name": "KillAll", "command": 'docker stop $(docker ps -aq) || true && docker rm $(docker ps -aq) || true && ( [ "$(docker ps -q)" ] || docker rmi $(docker images -q) || true ) && ( [ "$(docker images -q)" ] || docker system prune -a --volumes --force ) && docker network prune --force || true'},
        {"name": "Pull Docker Image", "command": "docker pull michadockermisha/backup:<choosename>"},
        {"name": "Run Docker Container", "command": "docker run -v /mnt/c/:/c/ -it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -it --name <choosename> michadockermisha/backup:<choosename><endcommand>"},
        {"name": "Create Dockerfile", "command": "echo '# Use a base image\nFROM alpine:latest\n\n# Install rsync\nRUN apk --no-cache add rsync\n\n# Set the working directory\nWORKDIR /app\n\n# Copy everything within the current path to /home/\nCOPY . /home/\n\n# Default runtime options\nCMD [\"rsync\", \"-aP\", \"/home/\", \"/home/\"]' > Dockerfile"},
        {"name": "Build Docker Image", "command": "docker build -t michadockermisha/backup:<choosename> ."},
        {"name": "Push Docker Image", "command": "docker push michadockermisha/backup:<choosename>"},
        {"name": "Compose up", "command": "docker-compose up -d <choosename>"},
        {"name": "Compose down", "command": "docker-compose down"},
        {"name": "Start container", "command": "docker exec -it <choosename> <endcommand>"},
        {"name": "Container IP", "command": "docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <choosename>"},
        {"name": "Show Containers Running", "command": "docker ps --size"},
        {"name": "Show ALL Containers", "command": "docker ps -a --size"},
        {"name": "Show Images", "command": "docker images"},
        {"name": "SEARCH", "command": "docker search <searchterm>"},
        {"name": "Update choco Packages", "command": "sudo apt update && sudo apt upgrade -y"},
        {"name": "Scan System Health", "command": "sudo systemctl status --full --no-pager"},
        {"name": "Restore System Health", "command": "sudo journalctl --verify"},
    ]

    while True:
        print("\nDocker Menu:")
        for i, cmd in enumerate(commands, 1):
            print(f"{i}. {cmd['name']}")
        print("0. Exit")

        choice = get_input("\nEnter the numbers of the commands you want to run (comma-separated) or 0 to exit: ")
        
        if choice == '0':
            break

        selected_commands = []
        for num in choice.split(','):
            try:
                index = int(num.strip()) - 1
                if 0 <= index < len(commands):
                    cmd = commands[index]
                    command = cmd["command"]
                    
                    if '<choosename>' in command:
                        name = get_input("Enter name: ")
                        command = command.replace('<choosename>', name)
                        
                        if '<endcommand>' in command:
                            end_command = get_input("Enter end command (e.g., bash, sh) or leave blank: ")
                            end_command = f" {end_command}" if end_command else ""
                            command = command.replace('<endcommand>', end_command)
                    
                    elif '<searchterm>' in command:
                        search_term = get_input("Enter search term: ")
                        command = command.replace('<searchterm>', search_term)
                    
                    selected_commands.append(command)
                else:
                    print(f"Invalid number: {num}")
            except ValueError:
                print(f"Invalid input: {num}")

        if selected_commands:
            print("\nSelected commands:")
            for cmd in selected_commands:
                print(cmd)
            
            confirm = get_input("\nDo you want to run these commands? (y/n): ")
            if confirm.lower() == 'y':
                run_selected_commands(selected_commands)
            else:
                print("Commands not executed.")

if __name__ == "__main__":
    main()
