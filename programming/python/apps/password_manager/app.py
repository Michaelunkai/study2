from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import json
from cryptography.fernet import Fernet
import secrets
import string

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Used for session management

# Hardcoded credentials for login
USERNAME = "michaelovsky5"
PASSWORD = "123456"

class PasswordManager:
    def __init__(self):
        self.data_file = "passwords.json"
        self.key = self.load_key()
        self.fernet = Fernet(self.key)
        self.load_passwords()

    def load_key(self):
        """Load or generate a key for encryption."""
        if os.path.exists("secret.key"):
            return open("secret.key", "rb").read()
        else:
            key = Fernet.generate_key()
            with open("secret.key", "wb") as key_file:
                key_file.write(key)
            return key

    def load_passwords(self):
        """Load passwords from a JSON file."""
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as file:
                self.passwords = json.load(file)
        else:
            self.passwords = {}

    def save_passwords(self):
        """Save passwords to a JSON file."""
        with open(self.data_file, "w") as file:
            json.dump(self.passwords, file)

    def encrypt_password(self, password):
        """Encrypt a password."""
        return self.fernet.encrypt(password.encode()).decode()

    def decrypt_password(self, encrypted_password):
        """Decrypt a password."""
        return self.fernet.decrypt(encrypted_password.encode()).decode()

    def add_password(self, service, password):
        """Add a new password."""
        encrypted_password = self.encrypt_password(password)
        self.passwords[service] = encrypted_password
        self.save_passwords()

    def get_password(self, service):
        """Retrieve a password."""
        if service in self.passwords:
            return self.decrypt_password(self.passwords[service])
        else:
            return None

    def generate_password(self, length=12):
        """Generate a random password."""
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(characters) for _ in range(length))

manager = PasswordManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    """Login page."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password. Please try again.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout route."""
    session.clear()
    return redirect(url_for('login'))

@app.route('/index')
def index():
    """Password Manager main page."""
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_password():
    """Add password route."""
    service = request.form.get('service')
    password = request.form.get('password')
    manager.add_password(service, password)
    return redirect(url_for('index'))

@app.route('/retrieve', methods=['POST'])
def retrieve_password():
    """Retrieve password route."""
    service = request.form.get('service')
    password = manager.get_password(service)
    if password:
        return {"password": password}
    return {"error": "No password found for the service"}

@app.route('/generate', methods=['POST'])
def generate_password():
    """Generate password route."""
    length = int(request.form.get('length', 12))
    generated_password = manager.generate_password(length)
    return {"password": generated_password}

if __name__ == '__main__':
    app.run(debug=True)
