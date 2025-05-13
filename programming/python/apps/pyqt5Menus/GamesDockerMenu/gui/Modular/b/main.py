import sys
from PyQt5.QtWidgets import (
    QWidget, QApplication, QVBoxLayout, QHBoxLayout, QFileDialog, QLabel,
    QLineEdit, QStackedWidget, QScrollArea, QMessageBox, QInputDialog, QPushButton
)
from PyQt5.QtGui import QFont
from persistence import load_session, save_session
from dialogs import LoginDialog
from main_window import DockerApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QWidget {
            background-image: url(b.png);
            background-repeat: no-repeat;
            background-position: center;
            color: white;
        }
        QMenu, QInputDialog, QMessageBox {
            background-image: url(b.png);
            background-repeat: no-repeat;
            background-position: center;
            color: white;
        }
    """)
    font = QFont("Segoe UI", 12, QFont.Bold)
    app.setFont(font)
    
    session_data = load_session()
    if session_data is None:
        login = LoginDialog()
        if login.exec_() == login.Accepted:
            session_data = {
                "username": login.username,
                "login_password": login.login_password,
                "is_admin": login.is_admin
            }
            save_session(session_data)
        else:
            sys.exit(0)
    
    docker_app = DockerApp(session_data["login_password"], session_data["is_admin"], session_data["username"])
    docker_app.show()
    sys.exit(app.exec_())
