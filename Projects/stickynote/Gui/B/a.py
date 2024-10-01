import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, \
    QMessageBox, QAction, QShortcut
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont, QColor


class StickyNoteApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.createDatabase()
        self.loadNotes()

        # Create a timer to auto-save the note every 5 seconds
        self.timer = QTimer()
        self.timer.timeout.connect(self.autoSaveNote)
        self.timer.start(5000)  # 5000 milliseconds = 5 seconds

    def initUI(self):
        self.setWindowTitle('Sticky Note App')
        self.setGeometry(100, 100, 400, 400)

        # Set background color to yellow/gold
        self.setStyleSheet("background-color: rgb(255, 215, 0)")

        self.text_edit = QTextEdit()
        font = QFont("Lobster", 20, QFont.Bold)  # Set Lobster font, size 20, and bold
        self.text_edit.setFont(font)

        # Set text size to be 1.5 times smaller
        current_font = self.text_edit.font()
        current_font.setPointSize(int(current_font.pointSize() * 0.67))  # approximately 1.5 times smaller
        self.text_edit.setFont(current_font)

        self.save_button = QPushButton('Save')
        self.clear_button = QPushButton('Clear')
        self.close_button = QPushButton('Close')

        self.save_button.clicked.connect(self.saveNote)
        self.clear_button.clicked.connect(self.clearNote)
        self.close_button.clicked.connect(self.closeApp)

        self.createActions()
        self.createMenus()

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.close_button)

        central_widget = QWidget()
        central_widget.setLayout(QVBoxLayout())
        central_widget.layout().addWidget(self.text_edit)
        central_widget.layout().addLayout(button_layout)
        self.setCentralWidget(central_widget)

        self.createShortcuts()

    def createDatabase(self):
        self.conn = sqlite3.connect('notes.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS notes
                         (id INTEGER PRIMARY KEY, content TEXT)''')
        self.conn.commit()

    def createActions(self):
        self.save_action = QAction('Save', self)
        self.save_action.triggered.connect(self.saveNote)

        self.clear_action = QAction('Clear', self)
        self.clear_action.triggered.connect(self.clearNote)

        self.close_action = QAction('Close', self)
        self.close_action.triggered.connect(self.closeApp)

    def createMenus(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu('File')
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.clear_action)
        file_menu.addAction(self.close_action)

    def createShortcuts(self):
        save_shortcut = QShortcut('Ctrl+S', self)
        save_shortcut.activated.connect(self.saveNote)

        clear_shortcut = QShortcut('Ctrl+D', self)
        clear_shortcut.activated.connect(self.clearNote)

        close_shortcut = QShortcut('Ctrl+W', self)
        close_shortcut.activated.connect(self.closeApp)

    def saveNote(self):
        note_text = self.text_edit.toPlainText()
        if note_text:
            self.c.execute("INSERT INTO notes (content) VALUES (?)", (note_text,))
            self.conn.commit()
            QMessageBox.information(self, 'Note Saved', 'Note saved successfully!')
        else:
            QMessageBox.warning(self, 'Empty Note', 'Cannot save an empty note.')

    def loadNote(self):
        self.c.execute("SELECT content FROM notes")
        notes = self.c.fetchall()
        if notes:
            self.text_edit.setPlainText(notes[-1][0])

    def loadNotes(self):
        self.loadNote()

    def clearNote(self):
        self.text_edit.clear()

    def closeApp(self):
        self.conn.close()
        self.close()

    def autoSaveNote(self):
        note_text = self.text_edit.toPlainText()
        if note_text:
            self.c.execute("INSERT INTO notes (content) VALUES (?)", (note_text,))
            self.conn.commit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StickyNoteApp()
    window.show()
    sys.exit(app.exec_())
