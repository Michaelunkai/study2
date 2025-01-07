#!/usr/bin/python3

import os
from cryptography.fernet import Fernet

# Read the key from thekey.key
with open("thekey.key", "rb") as thekey:
    key = thekey.read()

# List all encrypted files
files = [file for file in os.listdir() if os.path.isfile(file) and file != "voldemort.py" and file != "thekey.key"]

secretphrase = "coffee"

user_phrase = input("Enter Secret Phrase\n")

if user_phrase == secretphrase:
    for file in files:
        with open(file, "rb") as thefile:
            contents_encrypted = thefile.read()
    
        try:
            contents_decrypted = Fernet(key).decrypt(contents_encrypted)
            with open(file, "wb") as thefile:
                thefile.write(contents_decrypted)
            print(f"Decrypted {file} successfully.")
        except Exception as e:
            print(f"Error decrypting {file}: {e}")
