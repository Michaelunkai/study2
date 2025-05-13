from PyQt5.QtWidgets import QPushButton, QFileDialog, QMessageBox
from backend import check_docker_engine, pull_docker_image, run_docker_command

class DockerCommands:
    def __init__(self, parent):
        self.parent = parent

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
        btn = QPushButton("Run Selected")
        btn.setStyleSheet("""
            QPushButton {
                background: #27AE60;
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background: #2ECC71;
            }
        """)
        btn.clicked.connect(self.run_selected_commands)
        return btn

    def select_destination_path(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        dialog.setOption(QFileDialog.ShowDirsOnly, True)
        if dialog.exec_():
            selected_dir = dialog.selectedFiles()[0]
            wsl_path = selected_dir.replace('\\', '/').replace('C:', '/mnt/c')
            return wsl_path
        return None

    def run_selected_commands(self):
        if not check_docker_engine():
            QMessageBox.warning(self.parent, "Docker Engine Not Running",
                                "Docker Engine is not running in WSL. Please start Docker in your Ubuntu WSL distribution and try again.")
            return
        selected_buttons = [btn for btn in self.parent.buttons if btn.isChecked() and btn.parent()]
        if not selected_buttons:
            QMessageBox.information(self.parent, "No Selection", "Please select at least one tag to run.")
            return
        destination_path = self.select_destination_path()
        if not destination_path:
            return
        reply = QMessageBox.question(self.parent, "Confirm Path",
                                     f"Selected destination path:\n{destination_path}\n\nProceed with the operation?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            return
        from PyQt5.QtCore import QThreadPool
        pool = QThreadPool.globalInstance()
        for btn in selected_buttons:
            tag = btn.tag_info["docker_name"]
            from PyQt5.QtCore import QRunnable, pyqtSlot
            class DockerPullWorker(QRunnable):
                def __init__(self, tag):
                    super().__init__()
                    self.tag = tag
                    self.is_running = True

                @pyqtSlot()
                def run(self):
                    try:
                        if self.is_running:
                            pull_docker_image(self.tag)
                    except Exception as e:
                        print(f"DockerPullWorker error: {e}")
                    finally:
                        self.is_running = False
            pull_worker = DockerPullWorker(tag)
            pool.start(pull_worker)
        for btn in selected_buttons:
            tag = btn.tag_info["docker_name"]
            run_docker_command(tag, destination_path)
            btn.setChecked(False)
        QMessageBox.information(self.parent, "Run Initiated",
                                f"All selected commands have been initiated.\nFiles will be copied to: {destination_path}")
