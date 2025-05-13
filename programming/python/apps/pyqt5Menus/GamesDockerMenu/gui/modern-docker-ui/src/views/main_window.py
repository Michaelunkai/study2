from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from components.containers import MainContainer
from components.navigation import NavigationBar
from utils.constants import APP_TITLE

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        navigation_bar = NavigationBar()
        layout.addWidget(navigation_bar)

        main_container = MainContainer()
        layout.addWidget(main_container)

        self.show()