import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QComboBox, QMessageBox
)
from PyQt5.QtCore import Qt

from destination_manager import DestinationManager
from backend import run_docker_command

class GameSyncApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.destination_manager = DestinationManager(self)
        
        self.setWindowTitle("Game Sync Tool")
        self.setMinimumSize(600, 400)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Game selection section
        game_section = QWidget()
        game_layout = QHBoxLayout(game_section)
        game_label = QLabel("Select Game:")
        self.game_combo = QComboBox()
        
        # Add games from the games_data.json (for demo purposes, just adding a few)
        # In a real implementation, you would load these from games_data.json
        sample_games = ["witcher3", "eldenring", "oblivion", "fallout4"]
        self.game_combo.addItems(sample_games)
        
        game_layout.addWidget(game_label)
        game_layout.addWidget(self.game_combo)
        
        # Destination section
        destination_section = QWidget()
        destination_layout = QVBoxLayout(destination_section)
        
        destination_header = QLabel("Destination Directory:")
        
        destination_selector = QWidget()
        destination_selector_layout = QHBoxLayout(destination_selector)
        
        self.destination_label = QLabel(self.destination_manager.current_destination)
        self.destination_label.setStyleSheet("background-color: #f0f0f0; padding: 5px; border: 1px solid #ccc;")
        self.browse_button = QPushButton("Browse...")
        
        destination_selector_layout.addWidget(self.destination_label, 1)
        destination_selector_layout.addWidget(self.browse_button, 0)
        
        # Recent destinations
        recent_section = QWidget()
        recent_layout = QVBoxLayout(recent_section)
        recent_header = QLabel("Recent Destinations:")
        self.recent_combo = QComboBox()
        self.update_recent_destinations()
        
        recent_layout.addWidget(recent_header)
        recent_layout.addWidget(self.recent_combo)
        
        destination_layout.addWidget(destination_header)
        destination_layout.addWidget(destination_selector)
        destination_layout.addWidget(recent_section)
        
        # Action buttons
        buttons_section = QWidget()
        buttons_layout = QHBoxLayout(buttons_section)
        
        self.sync_button = QPushButton("Sync Game")
        self.sync_button.setMinimumHeight(40)
        self.sync_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        
        buttons_layout.addWidget(self.sync_button)
        
        # Add all sections to main layout
        main_layout.addWidget(game_section)
        main_layout.addWidget(destination_section)
        main_layout.addStretch(1)
        main_layout.addWidget(buttons_section)
        
        # Connect signals
        self.browse_button.clicked.connect(self.browse_destination)
        self.recent_combo.currentTextChanged.connect(self.select_recent_destination)
        self.sync_button.clicked.connect(self.sync_game)
        
    def update_recent_destinations(self):
        """Update the recent destinations dropdown"""
        self.recent_combo.clear()
        self.recent_combo.addItem("Select Recent...")
        recent = self.destination_manager.get_recent_destinations()
        if recent:
            self.recent_combo.addItems(recent)
    
    def browse_destination(self):
        """Open file browser to select destination directory"""
        directory = self.destination_manager.browse_for_destination()
        if directory:
            self.destination_label.setText(directory)
            self.update_recent_destinations()
    
    def select_recent_destination(self, path):
        """Set the selected recent destination as current"""
        if path and path != "Select Recent...":
            self.destination_label.setText(path)
            self.destination_manager.current_destination = path
    
    def sync_game(self):
        """Start the game synchronization process"""
        game_tag = self.game_combo.currentText()
        destination = self.destination_label.text()
        
        if not os.path.exists(destination):
            try:
                os.makedirs(destination, exist_ok=True)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not create destination directory: {e}")
                return
        
        try:
            # Save this destination for this game
            self.destination_manager.set_game_destination(game_tag, destination)
            
            # Run the docker command to sync the game
            run_docker_command(game_tag, destination)
            
            QMessageBox.information(
                self, 
                "Sync Started", 
                f"Game '{game_tag}' is being synchronized to:\n{destination}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start synchronization: {e}")

def main():
    app = QApplication(sys.argv)
    window = GameSyncApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
