import os
import json
from config import SESSION_FILE, SETTINGS_FILE, TABS_CONFIG_FILE, BANNED_USERS_FILE, ACTIVE_USERS_FILE, DEFAULT_TABS_CONFIG

def load_session():
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print("Error loading session file:", e)
    return None

def save_session(session_data):
    try:
        with open(SESSION_FILE, "w") as f:
            json.dump(session_data, f)
    except Exception as e:
        print("Error saving session file:", e)

def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print("Error loading settings file:", e)
    return {}

def save_settings(settings):
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f)
    except Exception as e:
        print("Error saving settings file:", e)

def load_tabs_config():
    if os.path.exists(TABS_CONFIG_FILE):
        try:
            with open(TABS_CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print("Error loading tabs config:", e)
    return DEFAULT_TABS_CONFIG

def save_tabs_config(config):
    try:
        with open(TABS_CONFIG_FILE, "w") as f:
            json.dump(config, f)
    except Exception as e:
        print("Error saving tabs config:", e)

def load_banned_users():
    if os.path.exists(BANNED_USERS_FILE):
        try:
            with open(BANNED_USERS_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print("Error loading banned users:", e)
    return []

def save_banned_users(banned):
    try:
        with open(BANNED_USERS_FILE, "w") as f:
            json.dump(banned, f)
    except Exception as e:
        print("Error saving banned users:", e)

def load_active_users():
    if os.path.exists(ACTIVE_USERS_FILE):
        try:
            with open(ACTIVE_USERS_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print("Error loading active users:", e)
    return {}

def save_active_users(users):
    try:
        with open(ACTIVE_USERS_FILE, "w") as f:
            json.dump(users, f)
    except Exception as e:
        print("Error saving active users:", e)
