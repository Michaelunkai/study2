import os

# Session & persistence filenames
SESSION_FILE = "user_session.json"
SETTINGS_FILE = "tag_settings.json"
TABS_CONFIG_FILE = "tabs_config.json"
BANNED_USERS_FILE = "banned_users.json"
ACTIVE_USERS_FILE = "active_users.json"

# Default tabs configuration
DEFAULT_TABS_CONFIG = [
    {"id": "all", "name": "All"},
    {"id": "finished", "name": "Finished"},
    {"id": "mybackup", "name": "MyBackup"},
    {"id": "not_for_me", "name": "Not for me right now"}
]
