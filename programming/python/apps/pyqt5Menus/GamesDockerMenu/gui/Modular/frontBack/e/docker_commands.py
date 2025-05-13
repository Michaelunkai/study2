import os
from PyQt5.QtWidgets import QPushButton, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, QRunnable, QObject, pyqtSignal, pyqtSlot
from backend import run_docker_command, pull_docker_image, run_with_real_time_output
from game_browser import GameDestinationDialog

class DockerCommandSignals(QObject):
    """Signals for Docker command execution."""
    finished = pyqtSignal(int)
    error = pyqtSignal(str)

class DockerCommandWorker(QRunnable):
    """Worker thread for executing Docker commands."""
    
    def __init__(self, app, command, is_docker=True):
        super().__init__()
        self.app = app
        self.command = command
        self.is_docker = is_docker
        self.signals = DockerCommandSignals()
    
    @pyqtSlot()
    def run(self):
        try:
            if self.is_docker:
                exit_code = self.app.docker_run_command_real_time(self.command)
            else:
                exit_code = self.app.rsync_command_real_time(self.command)
            self.signals.finished.emit(exit_code)
        except Exception as e:
            self.signals.error.emit(str(e))

class DockerCommands:
    def __init__(self, app):
        self.app = app
        self.run_button = None

    def create_browse_button(self):
        btn = QPushButton("Browse Path")
        btn.setStyleSheet("""
            QPushButton {
                background: #2980B9;
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #3498DB;
            }
        """)
        btn.clicked.connect(self.select_destination_path)
        return btn

    def create_run_button(self):
        self.run_button = QPushButton("Run Selected")
        self.run_button.setStyleSheet("""
            QPushButton {
                background-color: #2ECC71;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #27AE60;
            }
            QPushButton:disabled {
                background-color: #95A5A6;
            }
        """)
        self.run_button.clicked.connect(self.run_selected_tag)
        return self.run_button

    def select_destination_path(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        dialog.setOption(QFileDialog.ShowDirsOnly, True)
        if dialog.exec_():
            selected_dir = dialog.selectedFiles()[0]
            wsl_path = selected_dir.replace('\\', '/').replace('C:', '/mnt/c')
            return wsl_path
        return None

    def run_selected_tag(self):
        """Handle the action when the run button is clicked."""
        # Find the active/selected button
        active_button = None
        for button in self.app.buttons:
            if button.isChecked():
                active_button = button
                break
        
        if not active_button:
            QMessageBox.warning(self.app, "No Selection", "Please select a game first!")
            return
            
        tag_info = active_button.tag_info
        tag = tag_info["docker_name"]
        game_name = tag_info["alias"]
        
        # Open the destination dialog
        dialog = GameDestinationDialog(self.app, game_name, tag)
        if dialog.exec_() != GameDestinationDialog.Accepted:
            return  # User canceled
            
        destination_path = dialog.get_selected_path()
        if not destination_path:
            return  # No path selected
        
        # Show a message that we're starting the process
        QMessageBox.information(
            self.app, 
            "Starting Sync", 
            f"Starting to sync {game_name} to:\n{destination_path}\n\n"
            f"This will run in the background. Check your terminal for progress."
        )
        
        # Run the docker command with the selected destination path and ensure output is displayed
        run_docker_command(tag, destination_path)

    def on_run_command(self):
        selected_tags = []
        for tag, buttons in self.app.tag_buttons.items():
            for button in buttons:
                if button.isChecked():
                    selected_tags.append(button.tag_info)
        
        if not selected_tags:
            QMessageBox.warning(self.app, "No Selection", "Please select at least one tag.")
            return
        
        # Execute Docker command with real-time output directly
        for tag in selected_tags:
            docker_command = f"docker run -it {tag['docker_name']}"
            run_with_real_time_output(docker_command)
    
    def execute_rsync_command(self, source, destination):
        """Execute an rsync command with real-time output."""
        command = f"rsync -avz --progress {source} {destination}"
        run_with_real_time_output(command)
    
    def on_command_finished(self, exit_code):
        if exit_code == 0:
            print("Command completed successfully")
        else:
            print(f"Command failed with exit code: {exit_code}")
    
    def on_command_error(self, error_message):
        QMessageBox.warning(self.app, "Command Error", f"Error executing command: {error_message}")
        print(f"Error executing command: {error_message}")
