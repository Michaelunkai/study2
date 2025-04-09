import sys
import os
import winreg
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QListWidget, QWidget, QLabel, 
                             QFileDialog, QMessageBox, QListWidgetItem, QCheckBox)
from PyQt5.QtCore import Qt

class StartupManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Windows Startup Manager")
        self.setGeometry(100, 100, 800, 600)
        
        self.init_ui()
        self.load_startup_apps()
        
    def init_ui(self):
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Title label
        title_label = QLabel("Startup Applications")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # Startup apps list
        self.apps_list = QListWidget()
        self.apps_list.setStyleSheet("QListWidget { font-size: 14px; }")
        layout.addWidget(self.apps_list)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        # Disable button
        self.disable_button = QPushButton("Disable Selected")
        self.disable_button.clicked.connect(self.disable_selected)
        button_layout.addWidget(self.disable_button)
        
        # Enable button
        self.enable_button = QPushButton("Enable Selected")
        self.enable_button.clicked.connect(self.enable_selected)
        button_layout.addWidget(self.enable_button)
        
        # Add button
        self.add_button = QPushButton("Add Startup Program")
        self.add_button.clicked.connect(self.add_startup_program)
        button_layout.addWidget(self.add_button)
        
        # Remove button
        self.remove_button = QPushButton("Remove Selected")
        self.remove_button.clicked.connect(self.remove_selected)
        button_layout.addWidget(self.remove_button)
        
        layout.addLayout(button_layout)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: gray;")
        layout.addWidget(self.status_label)
    
    def load_startup_apps(self):
        self.apps_list.clear()
        
        # Load from registry (Current User)
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run") as key:
                i = 0
                while True:
                    try:
                        name, value, _ = winreg.EnumValue(key, i)
                        self.add_app_to_list(name, value, "Registry (Current User)", True)
                        i += 1
                    except OSError:
                        break
        except WindowsError:
            pass
        
        # Load from registry (Local Machine)
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run") as key:
                i = 0
                while True:
                    try:
                        name, value, _ = winreg.EnumValue(key, i)
                        self.add_app_to_list(name, value, "Registry (Local Machine)", True)
                        i += 1
                    except OSError:
                        break
        except WindowsError:
            pass
        
        # Load from startup folders
        startup_folders = [
            os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup'),
            os.path.join(os.getenv('PROGRAMDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        ]
        
        for folder in startup_folders:
            if os.path.exists(folder):
                for item in os.listdir(folder):
                    full_path = os.path.join(folder, item)
                    if os.path.isfile(full_path):
                        source = "Startup Folder (User)" if "AppData" in folder else "Startup Folder (All Users)"
                        self.add_app_to_list(item, full_path, source, True)
    
    def add_app_to_list(self, name, path, source, enabled):
        item = QListWidgetItem()
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Checkbox for enabled/disabled state
        checkbox = QCheckBox()
        checkbox.setChecked(enabled)
        checkbox.stateChanged.connect(lambda state, n=name, p=path, s=source: self.toggle_startup_app(n, p, s, state == Qt.Checked))
        layout.addWidget(checkbox)
        
        # App name
        name_label = QLabel(name)
        name_label.setMinimumWidth(200)
        layout.addWidget(name_label)
        
        # App path
        path_label = QLabel(path)
        path_label.setStyleSheet("color: gray;")
        path_label.setWordWrap(True)
        layout.addWidget(path_label)
        
        # Source
        source_label = QLabel(source)
        source_label.setStyleSheet("color: blue;")
        source_label.setMinimumWidth(150)
        layout.addWidget(source_label)
        
        widget.setLayout(layout)
        item.setSizeHint(widget.sizeHint())
        self.apps_list.addItem(item)
        self.apps_list.setItemWidget(item, widget)
    
    def toggle_startup_app(self, name, path, source, enable):
        try:
            if "Registry" in source:
                root = winreg.HKEY_CURRENT_USER if "(Current User)" in source else winreg.HKEY_LOCAL_MACHINE
                with winreg.OpenKey(root, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE) as key:
                    if enable:
                        winreg.SetValueEx(key, name, 0, winreg.REG_SZ, path)
                    else:
                        winreg.DeleteValue(key, name)
            else:
                # For startup folders, we would need to move files in/out of the folder
                # This is more complex, so we'll just show a message
                QMessageBox.information(self, "Info", "For startup folder items, please use the remove button to disable them.")
            
            self.status_label.setText(f"Updated: {name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update startup entry:\n{str(e)}")
            self.load_startup_apps()  # Refresh the list
    
    def disable_selected(self):
        for item in self.apps_list.selectedItems():
            widget = self.apps_list.itemWidget(item)
            checkbox = widget.findChild(QCheckBox)
            if checkbox and checkbox.isChecked():
                checkbox.setChecked(False)
    
    def enable_selected(self):
        for item in self.apps_list.selectedItems():
            widget = self.apps_list.itemWidget(item)
            checkbox = widget.findChild(QCheckBox)
            if checkbox and not checkbox.isChecked():
                checkbox.setChecked(True)
    
    def add_startup_program(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Application", "", "Executable Files (*.exe);;All Files (*)")
        
        if file_path:
            name_dialog = QMessageBox(self)
            name_dialog.setWindowTitle("Enter Startup Name")
            name_dialog.setText("Enter a name for the startup entry:")
            name_dialog.setIcon(QMessageBox.Question)
            name_dialog.addButton(QMessageBox.Ok)
            name_dialog.addButton(QMessageBox.Cancel)
            
            name_input = QLineEdit(os.path.basename(file_path))
            layout = name_dialog.layout()
            layout.addWidget(name_input, 0, 1)
            
            if name_dialog.exec_() == QMessageBox.Ok:
                name = name_input.text().strip()
                if name:
                    try:
                        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE) as key:
                            winreg.SetValueEx(key, name, 0, winreg.REG_SZ, file_path)
                        self.status_label.setText(f"Added: {name} to startup")
                        self.load_startup_apps()
                    except Exception as e:
                        QMessageBox.critical(self, "Error", f"Failed to add startup entry:\n{str(e)}")
    
    def remove_selected(self):
        selected_items = self.apps_list.selectedItems()
        if not selected_items:
            return
            
        reply = QMessageBox.question(self, "Confirm Removal", 
                                    f"Are you sure you want to remove {len(selected_items)} selected startup item(s)?",
                                    QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            for item in selected_items:
                widget = self.apps_list.itemWidget(item)
                source_label = widget.findChild(QLabel, None, 2)  # Third widget is the source label
                name_label = widget.findChild(QLabel, None, 0)  # First widget after checkbox is name
                
                if source_label and name_label:
                    source = source_label.text()
                    name = name_label.text()
                    
                    try:
                        if "Registry" in source:
                            root = winreg.HKEY_CURRENT_USER if "(Current User)" in source else winreg.HKEY_LOCAL_MACHINE
                            with winreg.OpenKey(root, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE) as key:
                                winreg.DeleteValue(key, name)
                        else:
                            # For startup folder items
                            path_label = widget.findChild(QLabel, None, 1)  # Second widget after checkbox is path
                            if path_label:
                                os.remove(path_label.text())
                        
                        self.status_label.setText(f"Removed: {name}")
                    except Exception as e:
                        QMessageBox.critical(self, "Error", f"Failed to remove {name}:\n{str(e)}")
            
            self.load_startup_apps()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StartupManager()
    window.show()
    sys.exit(app.exec_())
