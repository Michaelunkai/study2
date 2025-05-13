import sys
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtCore import QProcess, pyqtSlot, Qt
from PyQt5.QtGui import QTextCursor

class TerminalWidget(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Mimic PowerShell look: blue background with white text
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: #012456;
                color: white;
                font-family: Consolas, monospace;
                font-size: 12pt;
            }
        """)
        self.setReadOnly(True)
        self.processes = []  # Keep references to running processes
        self.appendPlainText("=== Terminal Started ===\n")

    def run_command(self, command):
        """Run a command asynchronously and show its real-time output."""
        self.appendPlainText(f"> {command}\n")
        process = QProcess(self)
        # Merge standard output and error channels
        process.setProcessChannelMode(QProcess.MergedChannels)
        process.finished.connect(lambda exitCode, exitStatus, proc=process: self.processes.remove(proc))
        process.readyRead.connect(lambda proc=process: self._append_output(proc))
        # Start command using PowerShell
        process.start("powershell.exe", ["-NoProfile", "-Command", command])
        self.processes.append(process)

    @pyqtSlot()
    def _append_output(self, process):
        try:
            data = process.readAll().data().decode()
            self.moveCursor(QTextCursor.End)
            self.insertPlainText(data)
            self.moveCursor(QTextCursor.End)
        except RuntimeError:
            # Occurs if the process has been deleted; safe to ignore.
            pass
