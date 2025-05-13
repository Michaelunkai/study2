from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class CustomDialog(QDialog):
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.init_ui(message)

    def init_ui(self, message):
        layout = QVBoxLayout(self)

        label = QLabel(message)
        layout.addWidget(label)

        button = QPushButton("Close")
        button.clicked.connect(self.close)
        layout.addWidget(button)

        self.setLayout(layout)