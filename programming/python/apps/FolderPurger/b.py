#!/usr/bin/env python3
import os
import sys
import ctypes
import subprocess
import time
import winreg
import psutil
from pathlib import Path
import signal

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

def get_process_list_using_path(path_to_check):
    """Get all processes that have a handle to the specified path"""
    using_processes = []
    path_to_check = path_to_check.lower()
    
    for proc in psutil.process_iter(['pid', 'name', 'open_files']):
        try:
            # Get open files for this process
            proc_info = proc.as_dict(attrs=['pid', 'name', 'open_files'])
            open_files = proc.open_files()
            
            # Check if any file path matches our target
            for file in open_files:
                if path_to_check in file.path.lower():
                    using_processes.append((proc_info['pid'], proc_info['name']))
                    break
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass
    
    return using_processes

def kill_process_tree(pid):
    """Kill a process and all its children"""
    try:
        parent = psutil.Process(pid)
        for child in parent.children(recursive=True):
            try:
                child.kill()
            except:
                pass
        parent.kill()
    except:
        pass

def force_kill_all_processes_using_folder(folder_path):
    """Aggressively kill all processes using any file in the folder"""
    print(f"Finding all processes using files in {folder_path}...")
    
    # Find processes using the folder or any file in it
    processes = get_process_list_using_path(folder_path)
    
    if processes:
        print(f"Found {len(processes)} processes using the folder:")
        for pid, name in processes:
            print(f" - PID {pid}: {name}")
            kill_process_tree(pid)
        time.sleep(2)  # Give processes time to terminate
    else:
        print("No processes found directly using the folder")
    
    # Try to identify processes by name related to the folder (more aggressive)
    folder_name = os.path.basename(folder_path).lower()
    
    # Kill any process with folder name in it
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if folder_name in proc.info['name'].lower():
                print(f"Killing possible related process: {proc.info['name']} (PID: {proc.info['pid']})")
                kill_process_tree(proc.info['pid'])
        except:
            pass

def take_ownership(path):
    """Take ownership of file or folder"""
    try:
        print(f"Taking ownership of {path}...")
        subprocess.run(f'takeown /f "{path}" /r /d y', shell=True)
        subprocess.run(f'icacls "{path}" /grant administrators:F /t', shell=True)
        return True
    except Exception as e:
        print(f"Error taking ownership: {e}")
        return False

def unlock_handle(path):
    """Try to unlock a file or folder using handle.exe if available"""
    # Look for handle.exe in common locations
    handle_exe = None
    search_paths = [
        ".",
        os.path.expanduser("~"),
        os.path.expanduser("~/Downloads"),
        "C:/SysinternalsSuite",
        "C:/Tools",
    ]
    
    for search_path in search_paths:
        check_path = os.path.join(search_path, "handle.exe")
        if os.path.exists(check_path):
            handle_exe = check_path
            break
    
    if not handle_exe:
        print("handle.exe not found for handle unlocking")
        return False
    
    try:
        print(f"Looking for handles to {path}...")
        # Just get the base name for matching
        base_name = os.path.basename(path)
        output = subprocess.check_output(f'"{handle_exe}" "{base_name}"', shell=True, stderr=subprocess.STDOUT).decode('utf-8', errors='ignore')
        
        # Process each line looking for handles
        handles_closed = False
        for line in output.splitlines():
            if base_name.lower() in line.lower():
                parts = line.split()
                if len(parts) >= 5:
                    try:
                        # Format is typically: pid: handle: type: flags: name
                        pid = None
                        for i, part in enumerate(parts):
                            if part.lower() == "pid:":
                                pid = int(parts[i+1])
                                break
                        
                        if pid:
                            print(f"Killing process {pid} with handle to {base_name}")
                            kill_process_tree(pid)
                            handles_closed = True
                    except:
                        pass
        
        return handles_closed
    except Exception as e:
        print(f"Error using handle.exe: {e}")
        return False

def force_purge_folder(folder_path):
    """Aggressively purge a folder and all its contents"""
    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} already deleted")
        return True
    
    print(f"\n===== AGGRESSIVE FOLDER PURGE =====")
    print(f"Target folder: {folder_path}")
    
    # Step 1: Kill all processes using the folder
    print("\nStep 1: Killing all processes using the folder...")
    force_kill_all_processes_using_folder(folder_path)
    
    # Step 2: Stop any related services
    print("\nStep 2: Stopping any related services...")
    try:
        # Try to find services related to the folder name
        folder_name = os.path.basename(folder_path).lower()
        services_output = subprocess.check_output("sc query type= service state= all", shell=True).decode('utf-8', errors='ignore')
        for line in services_output.splitlines():
            if "SERVICE_NAME:" in line:
                service_name = line.split(":", 1)[1].strip()
                if folder_name in service_name.lower():
                    try:
                        print(f"Stopping service: {service_name}")
                        subprocess.run(f"net stop {service_name} /y", shell=True)
                        subprocess.run(f"sc config {service_name} start= disabled", shell=True)
                    except:
                        pass
    except:
        pass
    
    # Step 3: Take ownership of the folder
    print("\nStep 3: Taking ownership of folder...")
    take_ownership(folder_path)
    
    # Step 4: Try to unlock any handles to the folder
    print("\nStep 4: Unlocking handles...")
    unlock_handle(folder_path)
    
    # Step 5: Force delete folder using multiple methods
    print("\nStep 5: Attempting folder deletion...")
    
    # Method 1: Try normal Python deletion
    try:
        import shutil
        shutil.rmtree(folder_path)
        if not os.path.exists(folder_path):
            print("Successfully deleted folder!")
            return True
    except Exception as e:
        print(f"Standard deletion failed: {e}")
    
    # Method 2: Try with rd command
    try:
        subprocess.run(f'rd /s /q "{folder_path}"', shell=True)
        if not os.path.exists(folder_path):
            print("Successfully deleted folder using rd command!")
            return True
    except:
        pass
    
    # Method 3: Try with more aggressive Command Prompt commands
    try:
        # First clear read-only flags
        subprocess.run(f'attrib -r -s -h "{folder_path}\\*.*" /s /d', shell=True)
        
        # Try DEL with force flag
        subprocess.run(f'del /f /s /q "{folder_path}\\*.*"', shell=True)
        
        # Try to remove the directory
        subprocess.run(f'rd /s /q "{folder_path}"', shell=True)
        
        if not os.path.exists(folder_path):
            print("Successfully deleted folder using aggressive commands!")
            return True
    except:
        pass
    
    # Method 4: File-by-file deletion (VERY aggressive)
    print("\nStep 6: Attempting file-by-file deletion...")
    try:
        # First list everything
        for root, dirs, files in os.walk(folder_path, topdown=False):
            # First delete files
            for file in files:
                try:
                    file_path = os.path.join(root, file)
                    print(f"Deleting file: {file_path}")
                    
                    # Try to clear file attributes
                    subprocess.run(f'attrib -r -s -h "{file_path}"', shell=True)
                    
                    # Try to close any handles to the file
                    unlock_handle(file_path)
                    
                    # Try to delete with various methods
                    try:
                        os.remove(file_path)
                    except:
                        try:
                            subprocess.run(f'del /f /q "{file_path}"', shell=True)
                        except:
                            pass
                except:
                    pass
            
            # Then try to remove directories
            for dir_name in dirs:
                try:
                    dir_path = os.path.join(root, dir_name)
                    print(f"Removing directory: {dir_path}")
                    os.rmdir(dir_path)
                except:
                    try:
                        subprocess.run(f'rd /s /q "{dir_path}"', shell=True)
                    except:
                        pass
        
        # Finally try to remove the main folder
        try:
            os.rmdir(folder_path)
        except:
            subprocess.run(f'rd /s /q "{folder_path}"', shell=True)
    except:
        pass
    
    # Final check
    if not os.path.exists(folder_path):
        print("\nSUCCESS: Folder has been completely purged!")
        return True
    
    # Last resort - nuclear option - create a batch file and run it with higher privileges
    print("\nStep 7: NUCLEAR OPTION - Creating a high-privilege batch purger...")
    try:
        # Create a batch file with elevated permissions
        batch_path = os.path.join(os.environ["TEMP"], "nuclear_purge.bat")
        with open(batch_path, "w") as f:
            f.write('@echo off\n')
            f.write('echo *** NUCLEAR FOLDER DELETION ***\n')
            f.write(f'echo Target: {folder_path}\n')
            f.write('echo.\n')
            
            # Take ownership
            f.write(f'takeown /f "{folder_path}" /r /d y\n')
            f.write(f'icacls "{folder_path}" /grant administrators:F /t\n')
            
            # Clear attributes
            f.write(f'attrib -r -s -h "{folder_path}\\*.*" /s /d\n')
            
            # Delete all files
            f.write(f'del /f /s /q "{folder_path}\\*.*"\n')
            
            # Remove all directories
            f.write(f'rd /s /q "{folder_path}"\n')
            
            # Check if folder still exists
            f.write('echo.\n')
            f.write(f'if exist "{folder_path}" (\n')
            f.write('  echo ERROR: Could not delete folder\n')
            f.write('  exit /b 1\n')
            f.write(') else (\n')
            f.write('  echo SUCCESS: Folder deleted\n')
            f.write('  exit /b 0\n')
            f.write(')\n')
        
        # Execute the batch file with highest privileges
        print(f"Executing nuclear purge batch file...")
        result = subprocess.run(
            f'powershell -Command "Start-Process cmd -ArgumentList \'/c, {batch_path}\' -Verb RunAs -Wait"',
            shell=True
        )
        
        # Check if folder is gone
        if not os.path.exists(folder_path):
            print("\nNUCLEAR PURGE SUCCESSFUL: Folder has been obliterated!")
            return True
        else:
            print("\nWARNING: Even nuclear option failed to delete the folder")
            return False
    except Exception as e:
        print(f"Nuclear option failed: {e}")
        return False

if __name__ == "__main__":
    # Check for admin rights
    run_as_admin()
    
    # Process command line arguments
    if len(sys.argv) < 2:
        print("Usage: python force_purge.py <folder_path> [--force]")
        print("Options:")
        print("  --force    Skip confirmation prompt")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    
    # Add a confirmation if not using --force
    if "--force" not in sys.argv:
        print(f"WARNING: This will AGGRESSIVELY delete {folder_path}")
        print("All processes using the folder will be terminated.")
        print("This operation CANNOT be undone!")
        confirm = input("Continue? (y/n): ")
        if confirm.lower() != 'y':
            print("Operation cancelled.")
            sys.exit(0)
    
    # Execute the force purge
    success = force_purge_folder(folder_path)
    
    if success:
        print("\n✅ SUCCESS: Folder has been completely deleted!")
        sys.exit(0)
    else:
        print("\n❌ FAILURE: Could not delete folder completely.")
        print("You may need to restart your computer to release all locks.")
        sys.exit(1)
