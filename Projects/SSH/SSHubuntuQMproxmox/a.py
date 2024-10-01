import sys
import paramiko
import time
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

class SSHClientWindow(QMainWindow):
    def __init__(self, hostname, username, password):
        super().__init__()
        self.hostname = hostname
        self.username = username
        self.password = password
        self.ssh_client = None
        self.ssh_session = None

        self.initUI()

        self.connect_ssh()

    def initUI(self):
        self.setWindowTitle("SSH Client")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        self.layout.addWidget(self.output_text)

        self.input_line = QLineEdit(self)
        self.input_line.returnPressed.connect(self.send_command)
        self.layout.addWidget(self.input_line)

        self.setGeometry(100, 100, 800, 600)

    def connect_ssh(self):
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh_client.connect(self.hostname, username=self.username, password=self.password)
            self.output_text.append(f"Successfully connected to {self.hostname}")

            self.ssh_session = self.ssh_client.invoke_shell()

            self.output_thread = threading.Thread(target=self.receive_output)
            self.output_thread.start()

            # Send 'sudo su' command
            self.ssh_session.send("sudo su\n")
            time.sleep(1)  # Wait for the sudo prompt

            # Send the password for 'sudo su'
            self.ssh_session.send(f"{self.password}\n")
            time.sleep(1)  # Wait for the shell to switch to root

        except Exception as e:
            self.output_text.append(f"Failed to connect: {e}")
            self.ssh_client.close()

    def receive_output(self):
        while True:
            if self.ssh_session.recv_ready():
                output = self.ssh_session.recv(1024).decode()
                if output:
                    self.output_text.append(output)

    def send_command(self):
        command = self.input_line.text() + "\n"
        self.ssh_session.send(command)
        self.input_line.clear()

        if command.strip().lower() == "exit":
            self.ssh_client.close()
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    hostname = "192.168.1.193"
    username = "ubuntu"
    password = "123456"

    main_window = SSHClientWindow(hostname, username, password)
    main_window.show()

    sys.exit(app.exec_())
