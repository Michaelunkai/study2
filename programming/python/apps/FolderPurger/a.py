#!/usr/bin/env python3
import os
import sys
import ctypes
import subprocess
import time
import winreg
import psutil
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
        print("Requesting administrative privileges...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)

def force_unlock_explorer_dll(dll_path):
    """Specialized function to unlock a DLL from Windows Explorer"""
    print(f"Attempting to unlock {dll_path} from Windows Explorer")
    dll_path = os.path.abspath(dll_path)
    
    # Method 1: Kill Explorer and unload DLLs
    print("STEP 1: Killing Explorer process...")
    try:
        # First kill all explorer.exe processes
        subprocess.run("taskkill /F /IM explorer.exe", shell=True)
        time.sleep(2)  # Give time for the process to fully terminate
        
        # Start a new explorer.exe process that won't load our target DLL
        subprocess.Popen("explorer.exe")
        time.sleep(1)
    except Exception as e:
        print(f"Error killing Explorer: {e}")
    
    # Method 2: Try to move the file to check if it's unlocked
    print("STEP 2: Testing if file is unlocked...")
    try:
        temp_path = f"{dll_path}.temp"
        os.rename(dll_path, temp_path)
        os.rename(temp_path, dll_path)
        print("File appears to be unlocked!")
        return True
    except Exception as e:
        print(f"File still locked: {e}")
    
    # Method 3: Try to kill specific handles using handle.exe if available
    print("STEP 3: Attempting to close specific handles...")
    try:
        # Look for handle.exe in common locations
        handle_exe = None
        search_paths = [
            ".",
            os.path.expanduser("~"),
            os.path.expanduser("~/Downloads"),
            "C:/SysinternalsSuite",
            "C:/Tools",
        ]
        
        for path in search_paths:
            check_path = os.path.join(path, "handle.exe")
            if os.path.exists(check_path):
                handle_exe = check_path
                break
                
        if handle_exe:
            # Get just the filename for matching
            dll_name = os.path.basename(dll_path)
            
            # Run handle.exe to find handles to the DLL
            try:
                output = subprocess.check_output(f'"{handle_exe}" "{dll_name}"', shell=True, stderr=subprocess.STDOUT).decode('utf-8', errors='ignore')
                
                # Extract PIDs from the output
                for line in output.splitlines():
                    if dll_name.lower() in line.lower():
                        parts = line.split()
                        for i, part in enumerate(parts):
                            if part.lower() == "pid:":
                                try:
                                    pid = int(parts[i+1])
                                    print(f"Found process {pid} using {dll_name}, killing it...")
                                    subprocess.run(f"taskkill /F /PID {pid}", shell=True)
                                except:
                                    pass
            except:
                print("Could not find handles using handle.exe")
        else:
            print("handle.exe not found, skipping handle detection")
    except Exception as e:
        print(f"Error in handle detection: {e}")
    
    # Method 4: Use the Unlocker approach - try to rename the file
    print("STEP 4: Attempting to rename the DLL...")
    try:
        # First try to create a batch file that will delete the file on reboot
        batch_path = os.path.join(os.environ["TEMP"], "unlock_delete.bat")
        with open(batch_path, "w") as f:
            f.write(f'@echo off\n')
            f.write(f'echo Waiting for system to initialize...\n')
            f.write(f'timeout /t 5 /nobreak\n')
            f.write(f'echo Attempting to delete {dll_path}...\n')
            f.write(f'del /F /Q "{dll_path}"\n')
            f.write(f'if exist "{dll_path}" (\n')
            f.write(f'  echo Could not delete file, trying with different method\n')
            f.write(f'  takeown /f "{dll_path}" /a\n')
            f.write(f'  icacls "{dll_path}" /grant administrators:F\n')
            f.write(f'  del /F /Q "{dll_path}"\n')
            f.write(f')\n')
            f.write(f'echo Cleanup complete\n')
        
        # Schedule the batch file to run at next startup using Task Scheduler
        task_name = "UnlockDLLTask"
        print(f"Scheduling deletion task to run at next system startup")
        subprocess.run(
            f'schtasks /create /tn "{task_name}" /tr "{batch_path}" /sc onstart /ru system /f',
            shell=True
        )
        
        # Try to rename the file with various techniques
        for i in range(5):
            try:
                new_name = f"{dll_path}.{i}.bak"
                os.rename(dll_path, new_name)
                print(f"Successfully renamed to {new_name}")
                
                # If renaming succeeded, we can try to delete the renamed file
                try:
                    os.remove(new_name)
                    print(f"Successfully deleted renamed file")
                    return True
                except:
                    print(f"Could not delete renamed file, but original file path is now clear")
                    return True
            except Exception as e:
                print(f"Rename attempt {i+1} failed: {e}")
                time.sleep(1)
    except Exception as e:
        print(f"Error in file renaming: {e}")
    
    # Method 5: Extreme approach - use the Microsoft Unlocker method
    print("STEP 5: Attempting to use bootexecute to delete the file on boot...")
    try:
        # Create a unique pendingdelete entry
        file_path_nt = dll_path.replace("\\", "\\\\")
        file_path_nt = "\\??\\" + file_path_nt
        
        # Use REG to modify PendingFileRenameOperations
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager", 0, winreg.KEY_ALL_ACCESS)
        
        try:
            value = winreg.QueryValueEx(key, "PendingFileRenameOperations")[0]
            # This is a REG_MULTI_SZ value, which is a null-terminated array of null-terminated strings
            if not value.endswith('\0\0'):
                value += '\0'
            value += f"{file_path_nt}\0\0"
        except:
            # Key doesn't exist, create it
            value = f"{file_path_nt}\0\0"
        
        winreg.SetValueEx(key, "PendingFileRenameOperations", 0, winreg.REG_MULTI_SZ, value)
        winreg.CloseKey(key)
        
        print("Successfully scheduled file for deletion on next boot")
        return True
    except Exception as e:
        print(f"Error scheduling deletion: {e}")
    
    return False

def terminate_all_explorer_processes():
    """Kill all Windows Explorer processes"""
    try:
        # Kill all explorer.exe processes
        subprocess.run("taskkill /F /IM explorer.exe", shell=True)
        time.sleep(1)
        
        # Double check and kill any remaining explorer processes
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if 'explorer.exe' in proc.info['name'].lower():
                    proc.kill()
            except:
                pass
    except:
        pass

def force_purge_iobit_folder(folder_path):
    """Specialized function to purge IObit Uninstaller folder"""
    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} already deleted")
        return True
    
    print(f"\n===== SPECIALIZED PURGE FOR IOBIT UNINSTALLER =====")
    print(f"Target folder: {folder_path}")
    
    # Step 1: Kill all IObit processes
    print("\nSTEP 1: Killing all IObit processes...")
    try:
        # Kill specific IObit processes
        process_names = ["IObitUninstaller.exe", "IObitUninstallerPortable.exe", "IObitUninstallerService.exe"]
        for proc in process_names:
            try:
                subprocess.run(f"taskkill /F /IM {proc}", shell=True)
            except:
                pass
        
        # Kill any process with IObit in name
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if 'iobit' in proc.info['name'].lower() or 'uninstall' in proc.info['name'].lower():
                    proc.kill()
            except:
                pass
    except:
        pass
    
    # Step 2: Stop IObit services
    print("\nSTEP 2: Stopping IObit services...")
    try:
        # First attempt specific service names
        service_names = ["IObitUninstaller", "IObitUninstallerService"]
        for service in service_names:
            try:
                subprocess.run(f"net stop {service}", shell=True)
                subprocess.run(f"sc config {service} start= disabled", shell=True)
            except:
                pass
        
        # Try to find services with IObit in the name
        services_output = subprocess.check_output("sc query type= service state= all", shell=True).decode('utf-8', errors='ignore')
        for line in services_output.splitlines():
            if "SERVICE_NAME:" in line:
                service_name = line.split(":", 1)[1].strip()
                if "iobit" in service_name.lower() or "uninstall" in service_name.lower():
                    try:
                        subprocess.run(f"net stop {service_name}", shell=True)
                        subprocess.run(f"sc config {service_name} start= disabled", shell=True)
                    except:
                        pass
    except:
        pass
    
    # Step 3: Find the UninstallExplorer.dll file
    print("\nSTEP 3: Looking for UninstallExplorer.dll...")
    target_dll = None
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower() == "uninstallexplorer.dll":
                target_dll = os.path.join(root, file)
                print(f"Found DLL at: {target_dll}")
                break
        if target_dll:
            break
    
    # Step 4: Terminate all Explorer processes
    print("\nSTEP 4: Terminating all Explorer processes...")
    terminate_all_explorer_processes()
    time.sleep(2)  # Give time for processes to exit
    
    # Step 5: Unlock the DLL file if found
    if target_dll and os.path.exists(target_dll):
        print("\nSTEP 5: Unlocking the DLL file...")
        force_unlock_explorer_dll(target_dll)
    
    # Step 6: Try removing the folder
    print("\nSTEP 6: Removing the IObit folder...")
    try:
        # First try normal deletion
        import shutil
        shutil.rmtree(folder_path)
        print("Successfully deleted folder!")
        return True
    except Exception as e:
        print(f"Standard deletion failed: {e}")
    
    # Step 7: Try batch deletion
    print("\nSTEP 7: Attempting batch command deletion...")
    try:
        subprocess.run(f'rd /s /q "{folder_path}"', shell=True)
        if not os.path.exists(folder_path):
            print("Successfully deleted folder using rd command!")
            return True
    except:
        pass
    
    # Step 8: File-by-file deletion
    print("\nSTEP 8: Attempting file-by-file deletion...")
    try:
        for root, dirs, files in os.walk(folder_path, topdown=False):
            # First delete files
            for file in files:
                try:
                    file_path = os.path.join(root, file)
                    # Clear attributes first
                    subprocess.run(f'attrib -r -s -h "{file_path}"', shell=True)
                    # Try to delete
                    os.remove(file_path)
                except:
                    pass
            
            # Then try to remove directories
            for dir in dirs:
                try:
                    dir_path = os.path.join(root, dir)
                    os.rmdir(dir_path)
                except:
                    pass
        
        # Try to remove the main folder
        try:
            os.rmdir(folder_path)
        except:
            pass
    except:
        pass
    
    # Step 9: Check if the folder is gone
    if not os.path.exists(folder_path):
        print("\nSUCCESS: Folder has been purged!")
        return True
    
    # Step 10: Last resort - schedule folder deletion on boot
    print("\nSTEP 10: Scheduling folder deletion on boot...")
    try:
        # Create a batch file to delete the folder on boot
        boot_batch = os.path.join(os.environ["TEMP"], "delete_iobit_folder.bat")
        with open(boot_batch, "w") as f:
            f.write('@echo off\n')
            f.write('echo Waiting for system startup...\n')
            f.write('timeout /t 10 /nobreak\n')
            f.write(f'echo Attempting to delete {folder_path}...\n')
            f.write(f'rd /s /q "{folder_path}"\n')
            f.write('echo Done\n')
        
        # Create scheduled task to run at startup
        subprocess.run(
            f'schtasks /create /tn "DeleteIObitFolder" /tr "{boot_batch}" /sc onstart /ru system /f',
            shell=True
        )
        
        print("\nWARNING: Folder still exists but will be deleted on next system boot")
        print("IMPORTANT: Please restart your computer to complete the deletion")
        return False
    except Exception as e:
        print(f"Failed to schedule deletion: {e}")
        return False

def restart_explorer():
    """Restart Windows Explorer"""
    try:
        # Start Explorer again
        subprocess.Popen("explorer.exe")
    except:
        pass

if __name__ == "__main__":
    # Check for admin rights
    run_as_admin()
    
    # Process command line arguments
    if len(sys.argv) < 2:
        print("Usage: python explorer_dll_killer.py <folder_path>")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    
    # Add a confirmation if not using --force
    if "--force" not in sys.argv:
        print(f"WARNING: This will aggressively delete {folder_path} and kill explorer.exe")
        print("Windows Explorer will be restarted automatically when done.")
        confirm = input("Continue? (y/n): ")
        if confirm.lower() != 'y':
            print("Operation cancelled.")
            sys.exit(0)
    
    # Execute the specialized purge
    success = force_purge_iobit_folder(folder_path)
    
    # Restart Explorer if it was killed
    restart_explorer()
    
    if success:
        print("\n✓ SUCCESS: IObit Uninstaller folder has been completely purged!")
    else:
        print("\n! PARTIAL SUCCESS: Folder will be deleted on next system restart")
        print("Please restart your computer to complete the purge operation.")
