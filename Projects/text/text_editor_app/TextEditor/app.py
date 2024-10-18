from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QFileDialog, QAction, QFontDialog, QShortcut, QColorDialog
from PyQt5.QtGui import QTextCharFormat, QFont, QKeySequence, QColor
from PyQt5.QtCore import Qt, QMimeData
import sys

class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.text_area = QTextEdit(self)
        self.setCentralWidget(self.text_area)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        open_action = QAction('Open', self)
        open_action.triggered.connect(self.openFile)
        file_menu.addAction(open_action)

        save_action = QAction('Save', self)
        save_action.triggered.connect(self.saveFile)
        file_menu.addAction(save_action)

        # Save shortcut (Ctrl + S)
        save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        save_shortcut.activated.connect(self.saveFile)

        edit_menu = menubar.addMenu('Edit')

        font_style_action = QAction('Change Font Style', self)
        font_style_action.triggered.connect(self.changeFontStyle)
        edit_menu.addAction(font_style_action)

        color_text_action = QAction('Change Text Color', self)
        color_text_action.triggered.connect(self.changeTextColor)
        edit_menu.addAction(color_text_action)

        color_bg_action = QAction('Change Background Color', self)
        color_bg_action.triggered.connect(self.changeBackgroundColor)
        edit_menu.addAction(color_bg_action)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Misha fedro Text Editor')

        # Apply custom style sheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: black;
            }
            QTextEdit {
                background-color: darkblue;
                color: white;
                border: 1px solid white;
            }
            QMenuBar {
                background-color: darkblue;
                color: white;
            }
            QMenuBar::item {
                background-color: darkblue;
                color: white;
                padding: 4px 8px;
            }
            QMenuBar::item:selected {
                background-color: blue;
            }
            QMenu {
                background-color: darkblue;
                color: white;
            }
            QMenu::item:selected {
                background-color: blue;
            }
            #MainWindow {
                background-color: darkred;
            }
            #MainWindow QLabel {
                color: black;
            }
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            clipboard = QApplication.clipboard()
            mime_data = clipboard.mimeData()
            if mime_data.hasText():
                self.text_area.paste()
            else:
                event.ignore()
        else:
            super().mousePressEvent(event)

    def openFile(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'All Files (*);;Text Files (*.txt);;Python Files (*.py);;All Files (*)')
        if filename:
            with open(filename, 'r') as file:
                content = file.read()
                self.text_area.setPlainText(content)

    def saveFile(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'Text Files (*.txt);;Python Files (*.py);;All Files (*)')
        if filename:
            with open(filename, 'w') as file:
                content = self.text_area.toPlainText()
                file.write(content)

    def changeFontStyle(self):
        selected_text = self.text_area.textCursor().selectedText()
        if selected_text:
            font, ok = QFontDialog.getFont(self.text_area.font(), self, "Select Font Style")
            if ok:
                cursor = self.text_area.textCursor()
                format_ = QTextCharFormat()
                format_.setFont(font)
                format_.setFontWeight(QFont.Bold)
                cursor.mergeCharFormat(format_)

    def changeTextColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.text_area.setTextColor(color)

    def changeBackgroundColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.setStyleSheet(f"background-color: {color.name()};")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec_())
