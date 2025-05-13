import os
import json
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QFileDialog, QComboBox, QMessageBox, QApplication
)
from PyQt5.QtCore import Qt

class GameDestinationDialog(QDialog):
    """Dialog for selecting a destination path for a game"""
    
    RECENT_PATHS_FILE = "recent_destinations.json"
    DEFAULT_PATH = os.path.expanduser("~/Games")
    
    def __init__(self, parent=None, game_name="Game", tag_name="unknown"):
        super().__init__(parent)
        self.game_name = game_name
        self.tag_name = tag_name
        self.selected_path = ""
        self.recent_paths = self.load_recent_paths()
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI components"""
        self.setWindowTitle(f"Select Destination for {self.game_name}")
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout()
        
        # Game info
        info_label = QLabel(f"Please select where to download <b>{self.game_name}</b>")
        layout.addWidget(info_label)
        
        # Path selection
        path_layout = QHBoxLayout()
        
        self.path_label = QLabel(self.DEFAULT_PATH)
        self.path_label.setStyleSheet("background-color: #f0f0f0; padding: 8px; border: 1px solid #ddd;")
        self.path_label.setMinimumWidth(300)
        self.path_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_path)
        
        path_layout.addWidget(QLabel("Destination:"))
        path_layout.addWidget(self.path_label, 1)
        path_layout.addWidget(browse_btn)
        
        layout.addLayout(path_layout)
        
        # Recent paths
        if self.recent_paths:
            recent_layout = QHBoxLayout()
            recent_layout.addWidget(QLabel("Recent:"))
            
            self.recent_combo = QComboBox()
            self.recent_combo.addItem("-- Select Recent Path --")
            for path in self.recent_paths:
                self.recent_combo.addItem(path)
            self.recent_combo.currentTextChanged.connect(self.select_recent_path)
            
            recent_layout.addWidget(self.recent_combo, 1)
            layout.addLayout(recent_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        self.download_btn = QPushButton("Download Game")
        self.download_btn.setStyleSheet("background-color: #2980b9; color: white; font-weight: bold; padding: 8px;")
        self.download_btn.clicked.connect(self.accept)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addStretch(1)
        button_layout.addWidget(self.download_btn)
        
        layout.addStretch(1)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def browse_path(self):
        """Open a file dialog to browse for a destination directory"""
        path = QFileDialog.getExistingDirectory(
            self,
            "Select Destination Directory",
            self.path_label.text()
        )
        
        if path:
            self.path_label.setText(path)
            self.selected_path = path
    
    def select_recent_path(self, path):
        """Select a path from the recent paths dropdown"""
        if path and path != "-- Select Recent Path --":
            self.path_label.setText(path)
            self.selected_path = path
    
    def accept(self):
        """Handle the accept action (Download button)"""
        path = self.path_label.text()
        
        if not path:
            QMessageBox.warning(self, "No Path Selected", "Please select a destination path.")
            return
        
        # Check if directory exists, create if it doesn't
        try:
            os.makedirs(path, exist_ok=True)
            
            # Save to recent paths
            self.selected_path = path
            if path not in self.recent_paths:
                self.recent_paths.insert(0, path)
                # Keep only the 10 most recent paths
                self.recent_paths = self.recent_paths[:10]
                self.save_recent_paths()
                
            super().accept()
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Could not create or access the directory:\n{str(e)}"
            )
    
    def get_selected_path(self):
        """Return the selected path"""
        return self.selected_path
    
    def load_recent_paths(self):
        """Load the recent paths from file"""
        try:
            if os.path.exists(self.RECENT_PATHS_FILE):
                with open(self.RECENT_PATHS_FILE, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
            
        return []
        
    def save_recent_paths(self):
        """Save the recent paths to file"""
        try:
            with open(self.RECENT_PATHS_FILE, 'w') as f:
                json.dump(self.recent_paths, f)
        except Exception:
            pass
