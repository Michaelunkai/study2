import sys
import paramiko
import threading
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit
from PyQt5.QtGui import QTextCursor, QKeySequence
from PyQt5.QtCore import Qt, pyqtSignal, QObject

class TerminalOutput(QObject):
    output_received = pyqtSignal(str)

class Terminal(QMainWindow):
    def __init__(self, hostname, username, password):
        super().__init__()
        self.hostname = hostname
        self.username = username
        self.password = password
        self.ssh_client = None
        self.ssh_session = None
        self.terminal_output = TerminalOutput()
        self.initUI()
        self.connect_ssh()

    def initUI(self):
        self.setWindowTitle("SSH Terminal")
        self.setGeometry(100, 100, 1000, 800)

        self.terminal = QPlainTextEdit(self)
        self.terminal.setStyleSheet(
            "background-color: black; color: white; font-family: 'Courier New', monospace; font-size: 16px;")
        self.terminal.setReadOnly(True)
        self.terminal.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.terminal.setCursorWidth(2)

        self.setCentralWidget(self.terminal)

        self.command = ""
        self.command_history = []
        self.history_index = -1
        self.is_running = True

        self.terminal_output.output_received.connect(self.display_output)
        self.terminal.keyPressEvent = self.on_key_press
        self.terminal.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == event.KeyPress and obj == self.terminal:
            if event.matches(QKeySequence.Paste):
                self.on_paste()
                return True
        return super().eventFilter(obj, event)

    def on_key_press(self, event):
        if event.key() == Qt.Key_Return:
            self.terminal.appendPlainText("\n")
            self.execute_command(self.command)
            self.command = ""
        elif event.key() == Qt.Key_Backspace:
            if len(self.command) > 0:
                self.command = self.command[:-1]
                cursor = self.terminal.textCursor()
                cursor.deletePreviousChar()
        elif event.key() == Qt.Key_Up:
            if self.history_index > 0:
                self.history_index -= 1
                self.replace_current_command(self.command_history[self.history_index])
        elif event.key() == Qt.Key_Down:
            if self.history_index < len(self.command_history) - 1:
                self.history_index += 1
                self.replace_current_command(self.command_history[self.history_index])
            else:
                self.history_index = len(self.command_history)
                self.replace_current_command("")
        else:
            self.command += event.text()
            self.terminal.insertPlainText(event.text())

    def on_paste(self):
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        self.command += text
        self.terminal.insertPlainText(text)

    def execute_command(self, command):
        if command.strip().lower() == "exit":
            self.ssh_session.send(command + "\n")
            self.is_running = False
            self.close()
        elif command.strip().lower() == "clear":
            self.terminal.clear()
        else:
            self.ssh_session.send(command + "\n")
            self.command_history.append(command)
            self.history_index = len(self.command_history)

    def replace_current_command(self, command):
        self.command = command
        cursor = self.terminal.textCursor()
        cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)
        cursor.select(QTextCursor.LineUnderCursor)
        cursor.removeSelectedText()
        cursor.deletePreviousChar()
        self.terminal.insertPlainText(self.command)

    def connect_ssh(self):
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh_client.connect(self.hostname, username=self.username, password=self.password)
            self.ssh_session = self.ssh_client.invoke_shell()
            self.output_thread = threading.Thread(target=self.receive_output)
            self.output_thread.start()

            self.ssh_session.send("sudo su\n")
            self.ssh_session.send(f"{self.password}\n")
        except Exception as e:
            self.terminal.appendPlainText(f"Failed to connect: {e}")
            self.ssh_client.close()

    def receive_output(self):
        while self.is_running:
            if self.ssh_session.recv_ready():
                output = self.ssh_session.recv(65535).decode(errors='ignore')
                output = self.clean_output(output)
                self.terminal_output.output_received.emit(output)

    def display_output(self, output):
        self.terminal.moveCursor(QTextCursor.End)
        self.terminal.insertPlainText(output)
        self.terminal.moveCursor(QTextCursor.End)
        self.terminal.ensureCursorVisible()

    def clean_output(self, text):
        # Remove ANSI escape sequences and other unwanted characters
        ansi_escape = re.compile(r'''
            \x1B[@-_][0-?]*[ -/]*[@-~]  # Remove ANSI escape sequences
            | \r  # Remove carriage returns
            | \x0f  # Remove unwanted characters
        ''', re.VERBOSE)
        return ansi_escape.sub('', text)

    def closeEvent(self, event):
        self.is_running = False
        self.ssh_client.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    hostname = "192.168.1.193"
    username = "ubuntu"
    password = "123456"

    terminal = Terminal(hostname, username, password)
    terminal.show()

    sys.exit(app.exec_())
