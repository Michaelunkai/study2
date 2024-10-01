import os
import time
import subprocess
import psutil

def close_chrome():
    # Find and terminate all Chrome browser instances
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'chrome.exe':
            print(f"Closing Chrome with PID: {proc.info['pid']}")
            proc.terminate()  # Forcefully close Chrome browser

def run_linkedin():
    while True:
        # Ensure any existing Chrome browser is closed before starting a new one
        print("Closing any existing Chrome browser instance...")
        close_chrome()

        print("Starting linkedin app in a new PowerShell window...")

        # Start a new PowerShell instance and run the linkedin command
        process = subprocess.Popen(["powershell.exe", "-NoExit", "linkedin"], shell=True)

        # Wait for 150 seconds (2.5 minutes)
        time.sleep(150)

        # After 150 seconds, restart the cycle
        print("Waiting for the next cycle...")

if __name__ == "__main__":
    run_linkedin()

