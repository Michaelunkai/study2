import os
import re
import fnmatch

# Define regular expressions for various types of credentials
regex_patterns = {
    "API_KEY": r'(?i)(api[_-]?key\s*[=:]\s*["\']?[A-Za-z0-9_-]+["\']?)',
    "PASSWORD": r'(?i)(password\s*[=:]\s*["\']?[A-Za-z0-9@#$%^&*()_+=-]+["\']?)',
    "SECRET": r'(?i)(secret\s*[=:]\s*["\']?[A-Za-z0-9_-]+["\']?)',
    "TOKEN": r'(?i)(token\s*[=:]\s*["\']?[A-Za-z0-9._-]+["\']?)'
}

# Common placeholder terms and patterns that should be ignored
placeholders = [
    "your_db_password", "password", "pass", "example", "changeme", 
    "placeholder", "mypassword", "admin", "root", "123456",
    "your-cloudflare-global-api-key", "ConvertTo-SecureString"
]

# Common patterns to ignore
ignore_patterns = [
    r'your[-_]?[a-z]+[-_]?[a-z]+',
    r'convertto[-_]securestring'
]

def is_placeholder(password):
    for placeholder in placeholders:
        if placeholder.lower() in password.lower():
            return True
    return False

def matches_ignore_patterns(password):
    for pattern in ignore_patterns:
        if re.search(pattern, password, re.IGNORECASE):
            return True
    return False

def scan_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
            found_credentials = []
            for cred_type, pattern in regex_patterns.items():
                matches = re.findall(pattern, content)
                for match in matches:
                    # Extract the actual value from the matched pattern
                    value = match.split('=')[-1].strip().strip('"\'')
                    if not is_placeholder(value) and not matches_ignore_patterns(value):
                        found_credentials.append((cred_type, value))
            return found_credentials
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return []

def scan_directory(path):
    results = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                credentials = scan_file(file_path)
                if credentials:
                    results.append((file_path, credentials))
    return results

def main():
    path = input("Enter the path to scan for credentials: ").strip()
    if not os.path.exists(path):
        print("The provided path does not exist.")
        return
    
    print(f"Scanning path: {path}")
    results = scan_directory(path)
    
    if results:
        print("\nFound potential credentials:")
        for file_path, credentials in results:
            print(f"\nFile: {file_path}")
            for cred_type, match in credentials:
                print(f"  {cred_type}: {match}")
    else:
        print("No potential credentials found.")

if __name__ == "__main__":
    main()
