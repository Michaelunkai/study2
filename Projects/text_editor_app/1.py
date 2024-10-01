from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QFileDialog, QAction
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

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Text Editor')

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec_())
