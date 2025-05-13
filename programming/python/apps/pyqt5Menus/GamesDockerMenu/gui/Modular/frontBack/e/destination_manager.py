import os
import json
from PyQt5.QtWidgets import QFileDialog

# Constants
DEFAULT_DESTINATIONS_FILE = "game_destinations.json"
DEFAULT_DESTINATION = os.path.expanduser("~\\Games")

class DestinationManager:
    """
    Manages game destination paths for syncing games
    """
    
    def __init__(self, parent=None):
        """
        Initialize the DestinationManager
        
        Args:
            parent: The parent widget for file dialogs
        """
        self.parent = parent
        self.destinations = self._load_destinations()
        self.current_destination = self.destinations.get("default", DEFAULT_DESTINATION)
        
        # Ensure the default destination exists
        os.makedirs(self.current_destination, exist_ok=True)
        
    def _load_destinations(self):
        """Load saved destination paths from file"""
        try:
            if os.path.exists(DEFAULT_DESTINATIONS_FILE):
                with open(DEFAULT_DESTINATIONS_FILE, 'r') as f:
                    return json.load(f)
            else:
                return {"default": DEFAULT_DESTINATION, "recent": []}
        except Exception as e:
            print(f"Error loading destinations: {e}")
            return {"default": DEFAULT_DESTINATION, "recent": []}
            
    def _save_destinations(self):
        """Save destination paths to file"""
        try:
            with open(DEFAULT_DESTINATIONS_FILE, 'w') as f:
                json.dump(self.destinations, f, indent=4)
        except Exception as e:
            print(f"Error saving destinations: {e}")
    
    def browse_for_destination(self):
        """
        Open a file dialog to browse for a destination directory
        
        Returns:
            str: Selected directory path or None if canceled
        """
        directory = QFileDialog.getExistingDirectory(
            self.parent,
            "Select Destination Directory for Game Sync",
            self.current_destination
        )
        
        if directory:
            # Add to recent destinations if not already there
            recent = self.destinations.get("recent", [])
            if directory in recent:
                recent.remove(directory)
            recent.insert(0, directory)
            # Keep only the 5 most recent destinations
            self.destinations["recent"] = recent[:5]
            self.current_destination = directory
            self._save_destinations()
            
        return directory if directory else None
    
    def get_destination(self, game_tag):
        """
        Get the destination path for a specific game tag
        
        Args:
            game_tag: The game tag
            
        Returns:
            str: The destination path for the game
        """
        # Check if this game has a specific destination
        game_destinations = self.destinations.get("games", {})
        if game_tag in game_destinations:
            return game_destinations[game_tag]
        
        # Otherwise return the current destination
        return self.current_destination
        
    def set_game_destination(self, game_tag, destination):
        """
        Set a specific destination for a game
        
        Args:
            game_tag: The game tag
            destination: The destination path
        """
        if "games" not in self.destinations:
            self.destinations["games"] = {}
        
        self.destinations["games"][game_tag] = destination
        self._save_destinations()
    
    def get_recent_destinations(self):
        """
        Get the list of recent destinations
        
        Returns:
            list: List of recent destination paths
        """
        return self.destinations.get("recent", [])
