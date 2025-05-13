import sys
import os
import winreg
import ctypes
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableWidget, QTableWidgetItem, 
                             QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QHeaderView, 
                             QFileDialog, QMessageBox, QCheckBox, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class StartupManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.startup_entries = []
        self.load_startup_entries()
        
    def init_ui(self):
        self.setWindowTitle('Windows Startup Manager')
        self.setMinimumSize(800, 500)
        
        # Create central widget and layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        
        # Create table for startup items
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Enabled', 'Name', 'Command', 'Registry Location'])
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        
        # Create button layout
        button_layout = QHBoxLayout()
        
        # Add buttons
        self.refresh_btn = QPushButton('Refresh')
        self.refresh_btn.clicked.connect(self.load_startup_entries)
        
        self.add_btn = QPushButton('Add New Startup Item')
        self.add_btn.clicked.connect(self.add_startup_item)
        
        self.remove_btn = QPushButton('Remove Selected')
        self.remove_btn.clicked.connect(self.remove_startup_item)
        
        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.remove_btn)
        
        # Add status label
        self.status_label = QLabel('Ready')
        
        # Add widgets to main layout
        main_layout.addWidget(self.table)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.status_label)
        
        self.setCentralWidget(central_widget)
        
    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
            
    def load_startup_entries(self):
        self.startup_entries = []
        self.table.setRowCount(0)
        
        # Registry locations to check
        registry_locations = [
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", "HKCU"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run", "HKLM"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\RunOnce", "HKCU-Once"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\RunOnce", "HKLM-Once")
        ]
        
        # Get startup items from registry
        for hkey, reg_path, location_name in registry_locations:
            try:
                reg_key = winreg.OpenKey(hkey, reg_path)
                for i in range(winreg.QueryInfoKey(reg_key)[1]):
                    try:
                        name, value, _ = winreg.EnumValue(reg_key, i)
                        self.startup_entries.append({
                            'name': name,
                            'command': value,
                            'location': location_name,
                            'enabled': True
                        })
                    except WindowsError:
                        continue
                winreg.CloseKey(reg_key)
            except WindowsError:
                continue
                
        # Check startup folder items
        startup_folders = [
            os.path.join(os.environ['APPDATA'], r'Microsoft\Windows\Start Menu\Programs\Startup'),
            os.path.join(os.environ['ALLUSERSPROFILE'], r'Microsoft\Windows\Start Menu\Programs\Startup')
        ]
        
        for folder in startup_folders:
            if os.path.exists(folder):
                for item in os.listdir(folder):
                    item_path = os.path.join(folder, item)
                    if item.endswith('.lnk') or item.endswith('.url'):
                        self.startup_entries.append({
                            'name': item,
                            'command': item_path,
                            'location': 'Startup Folder',
                            'enabled': True
                        })
        
        # Display entries in table
        self.table.setRowCount(len(self.startup_entries))
        for i, entry in enumerate(self.startup_entries):
            # Checkbox for enabled state
            chk_box = QCheckBox()
            chk_box.setChecked(entry['enabled'])
            chk_box.stateChanged.connect(lambda state, row=i: self.toggle_startup_item(row, state))
            self.table.setCellWidget(i, 0, chk_box)
            
            # Add name, command, location
            self.table.setItem(i, 1, QTableWidgetItem(entry['name']))
            self.table.setItem(i, 2, QTableWidgetItem(entry['command']))
            self.table.setItem(i, 3, QTableWidgetItem(entry['location']))
        
        self.status_label.setText(f"Loaded {len(self.startup_entries)} startup items")
            
    def toggle_startup_item(self, row, state):
        entry = self.startup_entries[row]
        
        # Need admin privileges to modify HKLM
        if entry['location'].startswith('HKLM') and not self.is_admin():
            QMessageBox.warning(self, "Admin Rights Required", 
                                "You need administrator privileges to modify this startup item.")
            # Reset checkbox state
            self.table.cellWidget(row, 0).setChecked(entry['enabled'])
            return
            
        enabled = state == Qt.Checked
        
        try:
            if entry['location'] == 'Startup Folder':
                # For items in the startup folder, we can rename them to .disabled extension
                file_path = entry['command']
                if enabled and file_path.endswith('.disabled'):
                    new_path = file_path[:-9]  # Remove .disabled extension
                    os.rename(file_path, new_path)
                    entry['command'] = new_path
                elif not enabled and not file_path.endswith('.disabled'):
                    new_path = file_path + '.disabled'
                    os.rename(file_path, new_path)
                    entry['command'] = new_path
            else:
                # For registry items, we need to modify the registry
                hkey = winreg.HKEY_CURRENT_USER if entry['location'].startswith('HKCU') else winreg.HKEY_LOCAL_MACHINE
                subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
                if entry['location'].endswith('Once'):
                    subkey = r"Software\Microsoft\Windows\CurrentVersion\RunOnce"
                    
                reg_key = winreg.OpenKey(hkey, subkey, 0, winreg.KEY_SET_VALUE)
                
                if enabled:
                    # Enable by adding/updating the registry value
                    winreg.SetValueEx(reg_key, entry['name'], 0, winreg.REG_SZ, entry['command'])
                else:
                    # Disable by deleting the registry value
                    try:
                        winreg.DeleteValue(reg_key, entry['name'])
                    except WindowsError:
                        pass
                        
                winreg.CloseKey(reg_key)
                
            # Update entry state
            entry['enabled'] = enabled
            self.status_label.setText(f"{'Enabled' if enabled else 'Disabled'} {entry['name']}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to modify startup item: {str(e)}")
            # Reset checkbox state
            self.table.cellWidget(row, 0).setChecked(entry['enabled'])
    
    def add_startup_item(self):
        # Select executable file
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Program", "", "Executable Files (*.exe);;All Files (*.*)"
        )
        
        if not file_path:
            return
            
        # Get file name without extension as default name
        default_name = os.path.splitext(os.path.basename(file_path))[0]
        
        # Ask for name and confirmation
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Add Startup Item")
        msg_box.setText(f"Add '{default_name}' to startup?")
        msg_box.setInformativeText("Choose where to add the startup entry:")
        
        # Add buttons for different locations
        current_user_btn = msg_box.addButton("Current User", QMessageBox.ActionRole)
        all_users_btn = msg_box.addButton("All Users", QMessageBox.ActionRole)
        cancel_btn = msg_box.addButton(QMessageBox.Cancel)
        
        msg_box.exec_()
        
        clicked_button = msg_box.clickedButton()
        
        if clicked_button == cancel_btn:
            return
            
        try:
            if clicked_button == current_user_btn:
                # Add to HKCU registry
                reg_key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Microsoft\Windows\CurrentVersion\Run",
                    0,
                    winreg.KEY_SET_VALUE
                )
                winreg.SetValueEx(reg_key, default_name, 0, winreg.REG_SZ, file_path)
                winreg.CloseKey(reg_key)
                
            elif clicked_button == all_users_btn:
                # Need admin privileges for HKLM
                if not self.is_admin():
                    QMessageBox.warning(self, "Admin Rights Required", 
                                      "You need administrator privileges to add startup items for all users.")
                    return
                    
                # Add to HKLM registry
                reg_key = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE,
                    r"Software\Microsoft\Windows\CurrentVersion\Run",
                    0,
                    winreg.KEY_SET_VALUE
                )
                winreg.SetValueEx(reg_key, default_name, 0, winreg.REG_SZ, file_path)
                winreg.CloseKey(reg_key)
                
            # Refresh the list
            self.load_startup_entries()
            self.status_label.setText(f"Added {default_name} to startup")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add startup item: {str(e)}")
    
    def remove_startup_item(self):
        selected_rows = set(index.row() for index in self.table.selectedIndexes())
        
        if not selected_rows:
            QMessageBox.information(self, "No Selection", "Please select a startup item to remove.")
            return
            
        # Confirm removal
        confirm = QMessageBox.question(
            self,
            "Confirm Removal",
            f"Remove {len(selected_rows)} startup item(s)?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm != QMessageBox.Yes:
            return
            
        removed_count = 0
        
        for row in sorted(selected_rows, reverse=True):
            entry = self.startup_entries[row]
            
            # Need admin privileges to modify HKLM
            if entry['location'].startswith('HKLM') and not self.is_admin():
                QMessageBox.warning(self, "Admin Rights Required", 
                                  "You need administrator privileges to remove this startup item.")
                continue
                
            try:
                if entry['location'] == 'Startup Folder':
                    # Remove file from startup folder
                    file_path = entry['command']
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    elif os.path.exists(file_path + '.disabled'):
                        os.remove(file_path + '.disabled')
                else:
                    # Remove from registry
                    hkey = winreg.HKEY_CURRENT_USER if entry['location'].startswith('HKCU') else winreg.HKEY_LOCAL_MACHINE
                    subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
                    if entry['location'].endswith('Once'):
                        subkey = r"Software\Microsoft\Windows\CurrentVersion\RunOnce"
                        
                    reg_key = winreg.OpenKey(hkey, subkey, 0, winreg.KEY_SET_VALUE)
                    
                    try:
                        winreg.DeleteValue(reg_key, entry['name'])
                        removed_count += 1
                    except WindowsError:
                        pass
                        
                    winreg.CloseKey(reg_key)
                    
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to remove {entry['name']}: {str(e)}")
        
        # Refresh the list
        self.load_startup_entries()
        self.status_label.setText(f"Removed {removed_count} startup item(s)")

def main():
    app = QApplication(sys.argv)
    window = StartupManager()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
