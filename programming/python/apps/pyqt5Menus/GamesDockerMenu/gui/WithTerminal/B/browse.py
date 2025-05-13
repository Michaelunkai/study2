from PyQt5.QtWidgets import QFileDialog

def get_destination_path(parent=None):
    """
    Opens a dialog for the user to choose a directory and returns the path.
    """
    dialog = QFileDialog(parent)
    dialog.setFileMode(QFileDialog.DirectoryOnly)
    dialog.setOption(QFileDialog.ShowDirsOnly, True)
    if dialog.exec_():
        return dialog.selectedFiles()[0]
    return None
