#!/usr/bin/env python3
import os
import sys
import ctypes
import subprocess
import time
import winreg
import psutil
import signal
import tempfile
import random
import string
from pathlib import Path

# Constants for COM file unlocking
COINIT_MULTITHREADED = 0x0
CLSCTX_ALL = 0x1 + 0x2 + 0x4 + 0x10

# Ensure we have admin rights
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if is_admin():
        return True
    else:
        print("【 ELEVATING PRIVILEGES 】")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{sys.argv[0]}" "{sys.argv[1]}"', None, 1)
        sys.exit(0)

def kill_process_tree(pid, include_parent=True):
    """Kill a process tree (including parent)"""
    try:
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        
        # Kill children
        for child in children:
            try:
                print(f"  └─ Killing child process {child.pid}: {child.name()}")
                child.kill()
            except:
                try:
                    os.kill(child.pid, signal.SIGKILL)
                except:
                    pass
        
        # Kill parent if requested
        if include_parent:
            print(f"  └─ Killing parent process {parent.pid}: {parent.name()}")
            try:
                parent.kill()
            except:
                try:
                    os.kill(parent.pid, signal.SIGKILL)
                except:
                    pass
                    
        return True
    except:
        return False

def force_kill_all_processes_using_folder(folder_path):
    """Ultra-aggressive process killing for anything using a folder"""
    print("\n【 TERMINATING ALL PROCESSES 】")
    print(f"Finding and eliminating ALL processes using {folder_path}...")
    
    killed_count = 0
    folder_path_lower = folder_path.lower()
    folder_name = os.path.basename(folder_path).lower()
    
    # First approach: Kill any process with open handles to the folder
    for proc in psutil.process_iter(['pid', 'name', 'open_files']):
        try:
            # Try to get the open files
            proc_files = proc.open_files()
            for file in proc_files:
                if folder_path_lower in file.path.lower():
                    print(f"• Process {proc.pid} ({proc.name()}) has handle to {file.path}")
                    kill_process_tree(proc.pid)
                    killed_count += 1
                    break
        except:
            pass
    
    # Second approach: Kill processes with similar names to the folder
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            proc_name = proc.name().lower()
            # Kill if folder name is in process name
            if folder_name in proc_name:
                print(f"• Process {proc.pid} ({proc.name()}) has name similar to folder")
                kill_process_tree(proc.pid)
                killed_count += 1
        except:
            pass
    
    # Third approach: Use handle.exe if available
    handle_exe = find_handle_exe()
    if handle_exe:
        try:
            output = subprocess.check_output(f'"{handle_exe}" "{folder_path}"', shell=True, stderr=subprocess.STDOUT).decode('utf-8', errors='ignore')
            for line in output.splitlines():
                if folder_name in line.lower():
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part.lower() == "pid:":
                            try:
                                pid = int(parts[i+1])
                                print(f"• Handle.exe found process {pid} using folder")
                                kill_process_tree(pid)
                                killed_count += 1
                            except:
                                pass
        except:
            pass
    
    # Fourth approach: Kill Explorer.exe if it might be using the folder
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.name().lower() == "explorer.exe":
                print(f"• Killing Explorer.exe (PID: {proc.pid}) to release shell handles")
                kill_process_tree(proc.pid)
                killed_count += 1
    except:
        pass
    
    # Start a new Explorer process after a delay
    time.sleep(1)
    try:
        subprocess.Popen("explorer.exe")
    except:
        pass
    
    print(f"Total processes terminated: {killed_count}")
    # Wait for processes to fully terminate
    time.sleep(2)

def find_handle_exe():
    """Try to find handle.exe in common locations"""
    search_paths = [
        ".",
        os.path.expanduser("~"),
        os.path.expanduser("~/Downloads"),
        "C:/SysinternalsSuite",
        "C:/Tools",
        "C:/Windows",
        "C:/Program Files",
        "C:/Program Files (x86)",
    ]
    
    for path in search_paths:
        check_path = os.path.join(path, "handle.exe")
        if os.path.exists(check_path):
            return check_path
    
    return None

def take_ultimate_ownership(path):
    """Take complete ownership of a file or folder"""
    print(f"\n【 TAKING OWNERSHIP 】")
    print(f"Claiming full control of {path}...")
    
    try:
        # Method 1: Using takeown command
        subprocess.run(f'takeown /f "{path}" /r /d y', shell=True, capture_output=True)
        
        # Method 2: Using icacls to grant full permissions
        subprocess.run(f'icacls "{path}" /grant administrators:F /t', shell=True, capture_output=True)
        subprocess.run(f'icacls "{path}" /grant Everyone:F /t', shell=True, capture_output=True)
        subprocess.run(f'icacls "{path}" /grant System:F /t', shell=True, capture_output=True)
        
        # Method 3: Clear all file attributes
        subprocess.run(f'attrib -r -s -h "{path}" /s /d', shell=True, capture_output=True)
        
        return True
    except Exception as e:
        print(f"Error taking ownership: {e}")
        return False

def create_random_string(length=8):
    """Create a random string for temporary filenames"""
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def create_nuclear_batch(folder_path):
    """Create an ultra-aggressive batch file to purge the folder"""
    temp_dir = tempfile.gettempdir()
    rand_suffix = create_random_string()
    batch_path = os.path.join(temp_dir, f"purge_{rand_suffix}.bat")
    
    with open(batch_path, "w") as f:
        f.write('@echo off\n')
        f.write('echo ════════════════════════════════════════════\n')
        f.write('echo        ULTIMATE FOLDER DESTRUCTION\n')
        f.write('echo ════════════════════════════════════════════\n')
        f.write(f'echo Target: {folder_path}\n\n')
        
        # 1. Kill processes
        f.write('echo Killing any remaining processes...\n')
        f.write('taskkill /F /IM explorer.exe\n')
        f.write(f'for /f "tokens=2" %%a in (\'handle "{folder_path}" ^| findstr /i "pid:"\') do (\n')
        f.write('    taskkill /F /PID %%a\n')
        f.write(')\n\n')
        
        # 2. Take ownership
        f.write('echo Taking ownership...\n')
        f.write(f'takeown /f "{folder_path}" /r /d y\n')
        f.write(f'icacls "{folder_path}" /grant administrators:F /t\n')
        f.write(f'icacls "{folder_path}" /grant everyone:F /t\n\n')
        
        # 3. Clear attributes
        f.write('echo Clearing attributes...\n')
        f.write(f'attrib -r -s -h "{folder_path}\\*.*" /s /d\n\n')
        
        # 4. Purge the folder
        f.write('echo Purging folder contents...\n')
        f.write(f'del /f /q /s "{folder_path}\\*.*"\n\n')
        
        # 5. Remove directory structure
        f.write('echo Removing directory structure...\n')
        f.write(f'rd /s /q "{folder_path}"\n\n')
        
        # 6. Double-check with robocopy (empty folder trick)
        f.write('echo Using robocopy empty folder trick...\n')
        f.write(f'mkdir "%TEMP%\\empty_{rand_suffix}"\n')
        f.write(f'robocopy "%TEMP%\\empty_{rand_suffix}" "{folder_path}" /MIR /R:1 /W:1\n')
        f.write(f'rd /s /q "{folder_path}"\n')
        f.write(f'rd /s /q "%TEMP%\\empty_{rand_suffix}"\n\n')
        
        # 7. Restart Explorer
        f.write('echo Restarting Explorer...\n')
        f.write('start explorer.exe\n\n')
        
        # 8. Final check
        f.write('echo Checking results...\n')
        f.write(f'if exist "{folder_path}" (\n')
        f.write('    echo [!] FAILED: Folder still exists\n')
        f.write('    echo Please restart your computer for complete removal\n')
        f.write(') else (\n')
        f.write('    echo [✓] SUCCESS: Folder completely purged!\n')
        f.write(')\n\n')
        
        f.write('pause\n')
    
    return batch_path

def multistage_folder_deletion(folder_path):
    """Perform multi-stage deletion of a folder"""
    print("\n【 MULTI-STAGE DELETION 】")
    
    # Stage 1: Python native deletion
    try:
        print("▶ Attempt 1: Native Python deletion")
        import shutil
        shutil.rmtree(folder_path, ignore_errors=True)
        if not os.path.exists(folder_path):
            print("  └─ Success!")
            return True
    except Exception as e:
        print(f"  └─ Failed: {e}")
    
    # Stage 2: Using OS commands directly
    try:
        print("▶ Attempt 2: Command line deletion")
        subprocess.run(f'rd /s /q "{folder_path}"', shell=True)
        if not os.path.exists(folder_path):
            print("  └─ Success!")
            return True
    except Exception as e:
        print(f"  └─ Failed: {e}")
    
    # Stage 3: File-by-file deletion
    print("▶ Attempt 3: File-by-file deletion")
    try:
        # Get all files first
        all_files = []
        try:
            for root, dirs, files in os.walk(folder_path, topdown=False):
                for file in files:
                    all_files.append(os.path.join(root, file))
        except:
            pass
        
        # Delete each file individually
        for file_path in all_files:
            try:
                print(f"  └─ Deleting: {file_path}")
                os.chmod(file_path, 0o777)  # Full permissions
                os.remove(file_path)
            except:
                try:
                    subprocess.run(f'del /f /q "{file_path}"', shell=True)
                except:
                    pass
        
        # Now remove directories bottom-up
        try:
            for root, dirs, files in os.walk(folder_path, topdown=False):
                for dir_name in dirs:
                    try:
                        dir_path = os.path.join(root, dir_name)
                        print(f"  └─ Removing dir: {dir_path}")
                        os.rmdir(dir_path)
                    except:
                        try:
                            subprocess.run(f'rd /s /q "{dir_path}"', shell=True)
                        except:
                            pass
            
            # Finally try to remove the root
            os.rmdir(folder_path)
        except:
            pass
        
        if not os.path.exists(folder_path):
            print("  └─ Success!")
            return True
    except Exception as e:
        print(f"  └─ Failed: {e}")
    
    # Stage 4: Robocopy empty folder trick
    print("▶ Attempt 4: Robocopy empty folder trick")
    try:
        # Create an empty folder
        temp_empty = os.path.join(tempfile.gettempdir(), f"empty_{create_random_string()}")
        os.makedirs(temp_empty, exist_ok=True)
        
        # Use robocopy to mirror the empty folder to target
        subprocess.run(f'robocopy "{temp_empty}" "{folder_path}" /MIR /R:1 /W:1', shell=True)
        
        # Try to remove the now-empty target folder
        os.rmdir(folder_path)
        os.rmdir(temp_empty)  # Clean up
        
        if not os.path.exists(folder_path):
            print("  └─ Success!")
            return True
    except Exception as e:
        print(f"  └─ Failed: {e}")
    
    # Stage 5: Nuclear option - execute special batch file
    print("▶ Attempt 5: Nuclear batch execution")
    try:
        batch_path = create_nuclear_batch(folder_path)
        print(f"  └─ Created nuclear batch: {batch_path}")
        
        # Execute the batch with highest privileges
        print("  └─ Executing nuclear batch file...")
        subprocess.run(
            f'powershell -Command "Start-Process cmd -ArgumentList \'/c, {batch_path}\' -Verb RunAs -Wait"',
            shell=True
        )
        
        # Check if folder is gone
        if not os.path.exists(folder_path):
            print("  └─ Success!")
            return True
    except Exception as e:
        print(f"  └─ Failed: {e}")
    
    # Stage 6: Last resort - register for deletion on reboot
    print("▶ Attempt 6: Register for deletion on next boot")
    try:
        # Create a special pending delete registry entry
        file_path_nt = folder_path.replace("\\", "\\\\")
        file_path_nt = "\\??\\" + file_path_nt
        
        # Use REG to modify PendingFileRenameOperations
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager", 0, winreg.KEY_ALL_ACCESS)
        
        try:
            value = winreg.QueryValueEx(key, "PendingFileRenameOperations")[0]
            if not value.endswith('\0\0'):
                value += '\0'
            value += f"{file_path_nt}\0\0"
        except:
            # Key doesn't exist, create it
            value = f"{file_path_nt}\0\0"
        
        winreg.SetValueEx(key, "PendingFileRenameOperations", 0, winreg.REG_MULTI_SZ, value)
        winreg.CloseKey(key)
        
        print("  └─ Scheduled for deletion on next boot")
        
        # Also create a startup task as backup
        boot_batch = os.path.join(tempfile.gettempdir(), f"boot_delete_{create_random_string()}.bat")
        with open(boot_batch, "w") as f:
            f.write('@echo off\n')
            f.write('timeout /t 10 /nobreak\n')
            f.write(f'rd /s /q "{folder_path}"\n')
        
        # Create scheduled task
        task_name = f"PurgeFolderTask_{create_random_string()}"
        subprocess.run(
            f'schtasks /create /tn "{task_name}" /tr "{boot_batch}" /sc onstart /ru system /f',
            shell=True,
            capture_output=True
        )
        
        print("  └─ Created boot-time deletion task")
        
        # Since this is our last attempt, we need to report failure
        return False
    except Exception as e:
        print(f"  └─ Failed: {e}")
        return False

def ultimate_folder_purge(folder_path):
    """Master function to utterly destroy a folder"""
    print("\n════════════════════════════════════════════")
    print("     ULTIMATE FOLDER PURGE INITIATED")
    print("════════════════════════════════════════════")
    print(f"Target: {folder_path}")
    
    if not os.path.exists(folder_path):
        print("\n✅ Folder already doesn't exist!")
        return True
    
    # Step 1: Kill all processes
    force_kill_all_processes_using_folder(folder_path)
    
    # Step 2: Take ownership
    take_ultimate_ownership(folder_path)
    
    # Step 3: Multi-stage deletion
    success = multistage_folder_deletion(folder_path)
    
    # Final report
    print("\n════════════════════════════════════════════")
    if success:
        print("✅ COMPLETE SUCCESS: Folder has been annihilated!")
        return True
    else:
        print("⚠️ PARTIAL SUCCESS: Folder will be removed on next boot")
        print("Please restart your computer to complete the purge")
        return False

if __name__ == "__main__":
    # Welcome message
    print("═════════════════════════════════════════════════════")
    print("  ULTIMATE FOLDER PURGER - 2000% PURGE GUARANTEED")
    print("═════════════════════════════════════════════════════")
    
    # Check for admin rights - no arguments needed since --force is automatic
    run_as_admin()
    
    # Get folder path from command line argument
    if len(sys.argv) < 2:
        print("Usage: python ultimate_purge.py <folder_path>")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    print(f"Target folder: {folder_path}")
    print("⚠️ WARNING: This folder will be COMPLETELY destroyed!")
    print("Operation will proceed automatically in 3 seconds...")
    time.sleep(3)
    
    # Execute the ultimate purge
    success = ultimate_folder_purge(folder_path)
    
    if success:
        sys.exit(0)
    else:
        print("\nRestart your computer now to complete the purge operation.")
        sys.exit(1)
