import subprocess
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QCheckBox, QPushButton, QInputDialog
from PyQt5.QtGui import QFont, QScreen
from PyQt5.QtCore import Qt

def run_command_as_admin(command):
    try:
        subprocess.Popen(command, shell=True, executable='/bin/bash')
    except Exception as e:
        print("Error:", e)

def run_selected_commands():
    selected_commands = []
    for cmd, var in zip(commands, command_vars):
        if var.isChecked():
            if '<choosename>' in cmd["command"]:
                name, ok_pressed = QInputDialog.getText(root, "Run", "Enter name:")
                if ok_pressed:
                    command = cmd["command"].replace('<choosename>', name)
                    if '<endcommand>' in command:
                        end_command, ok_pressed = QInputDialog.getText(root, "Run", "Enter end command (e.g., bash, sh) or leave blank:")
                        if ok_pressed:
                            end_command = f" {end_command}" if end_command else ""
                            command = command.replace('<endcommand>', end_command)
                    selected_commands.append(command)
            elif '<searchterm>' in cmd["command"]:
                search_term, ok_pressed = QInputDialog.getText(root, "Search", "Enter search term:")
                if ok_pressed:
                    command = cmd["command"].replace('<searchterm>', search_term)
                    selected_commands.append(command)
            else:
                selected_commands.append(cmd["command"])

    command_to_run = " && ".join(selected_commands)
    run_command_as_admin(command_to_run)

def choose_all(layout):
    for i in range(layout.count()):
        widget = layout.itemAt(i).widget()
        if isinstance(widget, QCheckBox):
            widget.setChecked(True)

def deselect_all(layout):
    for i in range(layout.count()):
        widget = layout.itemAt(i).widget()
        if isinstance(widget, QCheckBox):
            widget.setChecked(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    root = QWidget()
    root.setWindowTitle("MY linux")
    root.setStyleSheet("background-color: #f5f5dc;")

    tab_widget = QTabWidget()
    root_layout = QVBoxLayout(root)
    root_layout.addWidget(tab_widget)

    # Set font for tab titles
    tab_font = QFont("Lobster", 10, QFont.Bold)
    tab_widget.setFont(tab_font)

    # Initialize tabs for different commands
    docker_tab = QWidget()
    docker_layout = QVBoxLayout()
    docker_tab.setLayout(docker_layout)
    tab_widget.addTab(docker_tab, "Docker")

    bulk_tab = QWidget()
    bulk_layout = QVBoxLayout()
    bulk_tab.setLayout(bulk_layout)
    tab_widget.addTab(bulk_tab, "Bulk")

    # Create a new tab for WSL2 specific commands
    wsl2_tab = QWidget()
    wsl2_layout = QVBoxLayout()
    wsl2_tab.setLayout(wsl2_layout)
    tab_widget.addTab(wsl2_tab, "WSL2")

    command_vars = []

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

    current_path = subprocess.check_output("pwd", shell=True).decode('utf-8').strip()

    for cmd in commands:
        checkbox = QCheckBox(cmd['name'], parent=root)
        checkbox.setFont(QFont("Lobster", 10, QFont.Bold))
        command_vars.append(checkbox)

        if 'Docker' in cmd['name'] or 'KillAll' in cmd['name'] or 'Build' in cmd['name'] or 'Push' in cmd['name'] or 'Create' in cmd['name'] or 'Compose' in cmd['name'] or 'Start' in cmd['name'] or 'Container IP' in cmd['name'] or 'Show Containers Running' in cmd['name'] or 'Show ALL Containers' in cmd['name'] or 'Show Images' in cmd['name'] or 'SEARCH' in cmd['name']:
            docker_layout.addWidget(checkbox)
        else:
            bulk_layout.addWidget(checkbox)

    choose_all_button = QPushButton("Choose All", parent=root)
    choose_all_button.clicked.connect(lambda: choose_all(docker_layout))
    choose_all_button.setStyleSheet("background-color: black; color: white; font-weight: bold;")
    docker_layout.addWidget(choose_all_button)

    deselect_all_button = QPushButton("Deselect All", parent=root)
    deselect_all_button.clicked.connect(lambda: deselect_all(docker_layout))
    deselect_all_button.setStyleSheet("background-color: black; color: white; font-weight: bold;")
    docker_layout.addWidget(deselect_all_button)

    run_button = QPushButton("Run Selected Commands", parent=root)
    run_button.clicked.connect(run_selected_commands)
    run_button.setStyleSheet("background-color: black; color: white; font-weight: bold;")
    root_layout.addWidget(run_button)

    root.setLayout(root_layout)

    # Set window size and position
    screen_geometry = QScreen.availableGeometry(app.primaryScreen())
    width = screen_geometry.width() // 2
    height = screen_geometry.height() // 2
    root.setGeometry(
        screen_geometry.width() // 2 - width // 2,
        screen_geometry.height() // 2 - height // 2,
        width,
        height
    )

    root.show()

    sys.exit(app.exec_())
