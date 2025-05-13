#!import os
import sys
import ctypes
import subprocess
import time
import shutil
import tempfile
import random
import string
import signal
import psutil
import winreg
import re

# ---------- Helper Functions ----------

def is_admin():
    """Return True if the script is run as an administrator."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def run_as_admin():
    """Re-launch the script with admin privileges if not already."""
    if is_admin():
        return
    else:
        print("[*] Elevating privileges...")
        params = ' '.join(f'"{arg}"' for arg in sys.argv)
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
        sys.exit(0)

def create_random_string(length=8):
    """Return a random string of letters."""
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def kill_process(pid):
    """Kill process by PID; try normal then force kill."""
    try:
        p = psutil.Process(pid)
        p.kill()
    except Exception:
        try:
            os.kill(pid, signal.SIGKILL)
        except Exception:
            pass

def kill_process_tree(pid):
    """Kill a process and all its children."""
    try:
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        for child in children:
            try:
                print(f"[*] Killing child process {child.pid} ({child.name()})")
                child.kill()
            except Exception:
                kill_process(child.pid)
        print(f"[*] Killing parent process {parent.pid} ({parent.name()})")
        parent.kill()
    except Exception:
        pass

def kill_folder_processes(folder_path):
    """Find and kill any process that might have a handle on files under the folder."""
    folder_lower = folder_path.lower()
    killed = set()
    for proc in psutil.process_iter(['pid','name']):
        try:
            # If the process name contains a part of the folder name (heuristic)
            if os.path.basename(folder_path).lower() in proc.info['name'].lower():
                if proc.pid not in killed:
                    print(f"[*] Killing process {proc.pid} ({proc.info['name']}) because name hint")
                    kill_process_tree(proc.pid)
                    killed.add(proc.pid)
        except Exception:
            continue

    # Look for open files via psutil (if available)
    for proc in psutil.process_iter(['pid','open_files']):
        try:
            files = proc.open_files()
            for of in files:
                if folder_lower in of.path.lower():
                    if proc.pid not in killed:
                        print(f"[*] Killing process {proc.pid} (it holds {of.path})")
                        kill_process_tree(proc.pid)
                        killed.add(proc.pid)
                        break
        except Exception:
            continue

def take_ownership(folder_path):
    """Take ownership and grant full permissions over the folder recursively via system commands."""
    print("[*] Taking ownership and setting permissions...")
    try:
        subprocess.run(f'takeown         subprocess.run(f'icacls "{folder_path}"         subprocess.run(f'icacls "{folder_path}"     except Exception as e:
        print(f"[!] Error taking ownership: {e}")

# ---------- Deletion Stages ----------

def stage_python_rmtree(folder_path):
    """Attempt deletion using Python shutil.rmtree."""
    print("[*] Stage 1: Attempting Python rmtree deletion...")
    try:
        shutil.rmtree(folder_path, ignore_errors=True)
        if not os.path.exists(folder_path):
            print("[+] Python deletion succeeded!")
            return True
    except Exception as e:
        print(f"[!] rmtree failed: {e}")
    return False

def stage_cmd_delete(folder_path):
    """Attempt deletion using Windows command 'rd     print("[*] Stage 2: Attempting deletion via command line...")
    try:
        subprocess.run(f'rd         if not os.path.exists(folder_path):
            print("[+] Command line deletion succeeded!")
            return True
    except Exception as e:
        print(f"[!] Command deletion failed: {e}")
    return False

def stage_rename_then_delete(folder_path):
    """Rename folder (to bypass locks) then delete using shutil.rmtree."""
    print("[*] Stage 3: Renaming folder before deletion...")
    try:
        parent_dir = os.path.dirname(folder_path)
        new_name = os.path.join(parent_dir, f"del_{create_random_string()}")
        os.rename(folder_path, new_name)
        print(f"[*] Renamed to {new_name}. Now deleting...")
        shutil.rmtree(new_name, ignore_errors=True)
        if not os.path.exists(folder_path) and not os.path.exists(new_name):
            print("[+] Rename-then-delete succeeded!")
            return True
    except Exception as e:
        print(f"[!] Rename-then-delete failed: {e}")
    return False

def stage_nuclear_batch(folder_path):
    """Create and run a nuclear batch file that uses multiple techniques."""
    print("[*] Stage 4: Creating and executing nuclear deletion batch...")
    try:
        tmp_dir = tempfile.gettempdir()
        batch_file = os.path.join(tmp_dir, f"nuclear_{create_random_string()}.bat")
        with open(batch_file, "w") as f:
            f.write("@echo off\n")
            f.write("echo *** Nuking folder ***\n")
            # Kill common processes that can hold file handles
            f.write("taskkill             # Take ownership and remove attributes
            f.write(f'takeown             f.write(f'icacls "{folder_path}"             f.write(f'attrib -r -s -h "{folder_path}"             # Force delete
            f.write(f'rd             # Restart Explorer
            f.write("start explorer.exe\n")
            f.write("exit\n")
        # Run the batch file elevated
        subprocess.run(f'powershell -Command "Start-Process cmd -ArgumentList \'        if not os.path.exists(folder_path):
            print("[+] Nuclear batch deletion succeeded!")
            return True
    except Exception as e:
        print(f"[!] Nuclear batch deletion failed: {e}")
    return False

def stage_pending_delete(folder_path):
    """Last resort: schedule deletion on next reboot via registry modification."""
    print("[*] Stage 5: Scheduling folder for deletion on next reboot...")
    try:
        folder_nt = "\\??\\" + folder_path
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager", 0, winreg.KEY_SET_VALUE)
        try:
            value, typ = winreg.QueryValueEx(key, "PendingFileRenameOperations")
        except Exception:
            value = ""
        if isinstance(value, list):
            value.append(folder_nt)
        else:
            # If value is string or does not exist, create a list
            value = [folder_nt]
        winreg.SetValueEx(key, "PendingFileRenameOperations", 0, winreg.REG_MULTI_SZ, value)
        winreg.CloseKey(key)
        print("[*] Folder scheduled for deletion on reboot.")
        return True
    except Exception as e:
        print(f"[!] Scheduling deletion failed: {e}")
    return False

# ---------- Main Purge Function ----------

def purge_folder(folder_path):
    """Aggressively purge the specified folder with multiple attempts."""
    if not os.path.exists(folder_path):
        print("[*] Folder does not exist. Nothing to purge.")
        return True

    print("="*60)
    print(f"Starting purging process for: {folder_path}")
    print("="*60)

    # Step 0: Kill processes holding file locks on this folder
    kill_folder_processes(folder_path)

    # Step 1: Take ownership and clear attributes    take_ownership(folder_path)
    time.sleep(1)

    # Try a series of deletion stages
    if stage_python_rmtree(folder_path):
        return True
    if stage_cmd_delete(folder_path):
        return True
    if stage_rename_then_delete(folder_path):
        return True
    if stage_nuclear_batch(folder_path):
        return True
    if stage_pending_delete(folder_path):
        print("[*] The folder is scheduled to be removed after a reboot.")
        return True

    print("[!] Failed to completely purge the folder.")
    return False

# ---------- Main Script Execution ----------

if __name__ == "__main__":
    run_as_admin()

    if len(sys.argv) < 2:
        print("Usage: python code.py <full_path_to_folder>")
        sys.exit(1)
    target = sys.argv[1]

    print(f"WARNING: This operation will destroy the folder:\n  {target}\n")
    confirm = input("Continue? (y    if confirm.strip().lower() != 'y':
        print("Operation cancelled.")
        sys.exit(0)

    print("Proceeding in 3 seconds...")
    time.sleep(3)
    success = purge_folder(target)

    if success and not os.path.exists(target):
        print("\n[+] SUCCESS: Folder has been purged completely!")
        sys.exit(0)
    else:
        print("\n[!] PARTIAL SUCCESS: Folder may be removed after reboot.")
        sys.exit(1)

