from PyQt5.QtWidgets import QToolBar, QAction

class NavigationBar(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMovable(False)
        self.setStyleSheet("background-color: #2c3e50;")

        self.init_ui()

    def init_ui(self):
        self.add_action("Home", self.on_home_clicked)
        self.add_action("Settings", self.on_settings_clicked)
        self.add_action("About", self.on_about_clicked)

    def add_action(self, title, callback):
        action = QAction(title, self)
        action.triggered.connect(callback)
        self.addAction(action)

    def on_home_clicked(self):
        print("Home clicked")

    def on_settings_clicked(self):
        print("Settings clicked")

    def on_about_clicked(self):
        print("About clicked")