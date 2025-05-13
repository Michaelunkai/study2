import sys
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtCore import QProcess, pyqtSlot, Qt
from PyQt5.QtGui import QTextCursor

class TerminalWidget(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.processes = []  # Keep references to running QProcess instances
        self.appendPlainText("=== Terminal Started ===\n")

    def run_command(self, command):
        """Run a shell command asynchronously; append its output in real time."""
        self.appendPlainText(f"> {command}\n")
        process = QProcess(self)
        # Remove process from list when finished
        process.finished.connect(lambda exitCode, exitStatus, proc=process: self.processes.remove(proc))
        # Capture standard output
        process.readyReadStandardOutput.connect(lambda proc=process: self._append_output(proc))
        # Capture standard error
        process.readyReadStandardError.connect(lambda proc=process: self._append_output(proc, error=True))
        # Start process using PowerShell (adjust executable if needed)
        process.start("powershell.exe", ["-NoProfile", "-Command", command])
        self.processes.append(process)

    @pyqtSlot()
    def _append_output(self, process, error=False):
        if error:
            data = process.readAllStandardError().data().decode()
        else:
            data = process.readAllStandardOutput().data().decode()
        self.moveCursor(QTextCursor.End)
        self.insertPlainText(data)
        self.moveCursor(QTextCursor.End)
