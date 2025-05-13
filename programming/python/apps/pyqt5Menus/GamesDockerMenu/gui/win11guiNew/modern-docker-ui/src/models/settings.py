class AppSettings:
    def __init__(self):
        self.settings = {
            "theme": "light",
            "language": "en",
            "notifications": True,
        }

    def get_setting(self, key):
        return self.settings.get(key)

    def set_setting(self, key, value):
        self.settings[key] = value

    def load_settings(self, settings_dict):
        self.settings.update(settings_dict)

    def save_settings(self):
        # Placeholder for saving settings to a file or database
        pass