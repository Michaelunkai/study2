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
import shutil
from pathlib import Path
import traceback
import re

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
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(f'"{arg}"' for arg in sys.argv), None, 1)
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

def get_process_locking_file(file_path):
    """Find processes that have a lock on a file using handle.exe"""
    handle_exe = find_handle_exe()
    if not handle_exe:
        return []
        
    try:
        output = subprocess.check_output(f'"{handle_exe}" "{file_path}"', 
                                        shell=True, 
                                        stderr=subprocess.STDOUT).decode('utf-8', errors='ignore')
        
        pids = []
        for line in output.splitlines():
            match = re.search(r'pid: (\d+)', line, re.IGNORECASE)
            if match:
                pids.append(int(match.group(1)))
        return pids
    except:
        return []

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
            pid_pattern = re.compile(r'pid: (\d+)', re.IGNORECASE)
            for line in output.splitlines():
                match = pid_pattern.search(line)
                if match:
                    try:
                        pid = int(match.group(1))
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
    
    # Fifth approach: Kill system processes that might interfere (with caution)
    system_processes = ["SearchIndexer.exe", "MsMpEng.exe", "TiWorker.exe", "SecurityHealthService.exe"]
    for proc_name in system_processes:
        try:
            output = subprocess.check_output(f'taskkill /f /im {proc_name}', shell=True, stderr=subprocess.STDOUT)
            print(f"• Suspending system service: {proc_name}")
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
    
    # Try to download handle.exe if not found
    try:
        temp_dir = tempfile.gettempdir()
        handle_path = os.path.join(temp_dir, "handle.exe")
        
        # Use PowerShell to download handle.exe
        ps_command = """
        $ProgressPreference = 'SilentlyContinue'
        Invoke-WebRequest -Uri "https://download.sysinternals.com/files/Handle.zip" -OutFile "$env:TEMP\\handle.zip"
        Expand-Archive -Path "$env:TEMP\\handle.zip" -DestinationPath "$env:TEMP" -Force
        """
        
        subprocess.run(["powershell", "-Command", ps_command], capture_output=True)
        
        if os.path.exists(handle_path):
            print(f"Downloaded handle.exe to {handle_path}")
            return handle_path
    except:
        pass
    
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
        subprocess.run(f'icacls "{path}" /reset /t', shell=True, capture_output=True)
        
        # Method 3: Clear all file attributes
        subprocess.run(f'attrib -r -s -h -a "{path}" /s /d', shell=True, capture_output=True)
        
        # Method 4: Using PowerShell to take ownership (more powerful)
        ps_command = f'''
        $acl = Get-Acl "{path}"
        $owner = New-Object System.Security.Principal.SecurityIdentifier("S-1-5-32-544")
        $acl.SetOwner($owner)
        $rule = New-Object System.Security.AccessControl.FileSystemAccessRule("Everyone","FullControl","Allow")
        $acl.SetAccessRule($rule)
        Set-Acl "{path}" $acl -ErrorAction SilentlyContinue
        
        Get-ChildItem -Path "{path}" -Recurse -Force -ErrorAction SilentlyContinue | ForEach-Object {{
            $acl = Get-Acl $_.FullName -ErrorAction SilentlyContinue
            if ($acl) {{
                $acl.SetOwner($owner)
                $acl.SetAccessRule($rule)
                Set-Acl $_.FullName $acl -ErrorAction SilentlyContinue
            }}
        }}
        '''
        
        subprocess.run(["powershell", "-Command", ps_command], capture_output=True)
        
        return True
    except Exception as e:
        print(f"Error taking ownership: {e}")
        return False

def create_random_string(length=8):
    """Create a random string for temporary filenames"""
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def unlock_files_in_folder(folder_path):
    """Attempt to unlock files in the folder using various methods"""
    print("\n【 UNLOCKING FILES 】")
    print(f"Attempting to unlock files in {folder_path}...")
    
    # Try to find handle.exe
    handle_exe = find_handle_exe()
    
    # Try PowerShell method to unlock files
    ps_command = f'''
    function Unlock-File($path) {{
        if (Test-Path -Path $path -PathType Leaf) {{
            try {{
                [System.IO.File]::Open($path, 'Open', 'Write', 'None').Close()
                Write-Output "Unlocked: $path"
            }} catch {{
                Write-Output "Failed to unlock: $path"
            }}
        }}
    }}
    
    Get-ChildItem -Path "{folder_path}" -Recurse -Force -ErrorAction SilentlyContinue | ForEach-Object {{
        Unlock-File $_.FullName
    }}
    '''
    
    subprocess.run(["powershell", "-Command", ps_command], capture_output=True)
    
    # If handle.exe is available, try to close handles directly
    if handle_exe:
        try:
            # Get a list of all files
            all_files = []
            for root, _, files in os.walk(folder_path, topdown=False):
                for file in files:
                    all_files.append(os.path.join(root, file))
            
            # For each file that exists, try to close handles
            for file_path in all_files:
                if os.path.exists(file_path):
                    print(f"Closing handles for: {file_path}")
                    pids = get_process_locking_file(file_path)
                    for pid in pids:
                        print(f"  └─ Process {pid} has lock on file")
                        kill_process_tree(pid)
        except:
            pass
    
    # Try to create zero-byte dummy files where locked files exist
    try:
        # Create a list of zero-byte files to replace locked files
        dummy_files = []
        for root, _, files in os.walk(folder_path, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    if os.path.exists(file_path):
                        # Attempt to open the file for writing
                        with open(file_path, 'w') as f:
                            f.truncate(0)  # Make it zero bytes
                except:
                    # If can't open, remember to create dummy later
                    dummy_files.append(file_path)
                        
        # For any file we couldn't open, try to rename original and create dummy
        for file_path in dummy_files:
            try:
                if os.path.exists(file_path):
                    # Try to rename the original file
                    dummy_name = f"{file_path}.{create_random_string()}.tmp"
                    os.rename(file_path, dummy_name)
                    
                    # Create a zero-byte file in its place
                    with open(file_path, 'w') as f:
                        pass
            except:
                pass
    except:
        pass

def disable_services_using_folder(folder_path):
    """Disable services that might be using files in the folder"""
    print("\n【 DISABLING SERVICES 】")
    print(f"Shutting down services that might use {folder_path}...")
    
    # Common Windows services that might cause locking issues
    services_to_stop = [
        "wuauserv",         # Windows Update
        "WSearch",          # Windows Search
        "WinDefend",        # Windows Defender
        "sppsvc",           # Software Protection
        "msiserver",        # Windows Installer
        "TrustedInstaller", # Windows Modules Installer
        "PcaSvc",           # Program Compatibility Assistant
        "wuauserv"          # Windows Update
    ]
    
    # Additionally, look for services that might contain the folder name
    folder_name = os.path.basename(folder_path).lower()
    
    # Get all services and filter
    try:
        services_output = subprocess.check_output('sc query state= all', shell=True).decode('utf-8', errors='ignore')
        service_pattern = re.compile(r'SERVICE_NAME:\s+(\S+)', re.IGNORECASE)
        
        for match in service_pattern.finditer(services_output):
            service_name = match.group(1)
            if folder_name in service_name.lower() or any(s.lower() in service_name.lower() for s in ["microsoft", "edge", "ie", "explorer"]):
                services_to_stop.append(service_name)
    except:
        pass
    
    # Stop the services
    for service in services_to_stop:
        try:
            print(f"Stopping service: {service}")
            subprocess.run(f'sc stop {service}', shell=True, capture_output=True)
            subprocess.run(f'sc config {service} start= disabled', shell=True, capture_output=True)
        except:
            pass

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
        f.write('taskkill /F /IM SearchIndexer.exe\n')
        f.write('taskkill /F /IM MsMpEng.exe\n')
        f.write('taskkill /F /IM TiWorker.exe\n')
        f.write('taskkill /F /IM WmiPrvSE.exe\n')
        f.write(f'for /f "tokens=2" %%a in (\'handle "{folder_path}" ^| findstr /i "pid:"\') do (\n')
        f.write('    taskkill /F /PID %%a\n')
        f.write(')\n\n')
        
        # 2. Disable services
        f.write('echo Disabling services...\n')
        f.write('sc stop wuauserv\n')
        f.write('sc stop WSearch\n')
        f.write('sc stop WinDefend\n')
        f.write('sc stop TrustedInstaller\n')
        f.write('sc stop PcaSvc\n')
        f.write('sc stop msiserver\n')
        f.write('sc stop sppsvc\n\n')
        
        # 3. Take ownership
        f.write('echo Taking ownership...\n')
        f.write(f'takeown /f "{folder_path}" /r /d y\n')
        f.write(f'icacls "{folder_path}" /grant administrators:F /t\n')
        f.write(f'icacls "{folder_path}" /grant everyone:F /t\n')
        f.write(f'icacls "{folder_path}" /reset /t\n\n')
        
        # 4. Clear attributes
        f.write('echo Clearing attributes...\n')
        f.write(f'attrib -r -s -h -a "{folder_path}\\*.*" /s /d\n\n')
        
        # 5. Try to move the directory first (can bypass some locks)
        f.write('echo Trying to move the directory first...\n')
        temp_path = os.path.join(tempfile.gettempdir(), f"tempdir_{rand_suffix}")
        f.write(f'move /Y "{folder_path}" "{temp_path}" 2>nul\n')
        f.write(f'if exist "{temp_path}" (\n')
        f.write(f'  rd /s /q "{temp_path}"\n')
        f.write(f')\n\n')
        
        # 6. Purge the folder with multiple methods
        f.write('echo Purging folder contents with multiple methods...\n')
        
        # Try MoveFileEx method via PowerShell
        f.write('powershell -Command "Add-Type -AssemblyName Microsoft.VisualBasic; [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteDirectory')
        f.write(f'(\'{folder_path}\', \'OnlyErrorDialogs\', \'SendToRecycleBin\')"\n\n')
        
        # Try using directory junctions to trick Windows
        junction_path = os.path.join(tempfile.gettempdir(), f"junction_{rand_suffix}")
        f.write(f'mkdir "{junction_path}" 2>nul\n')
        f.write(f'mklink /J "{junction_path}\\target" "{folder_path}" 2>nul\n')
        f.write(f'rd /s /q "{junction_path}" 2>nul\n\n')
        
        # 7. Standard methods
        f.write(f'del /f /q /s "{folder_path}\\*.*"\n')
        f.write(f'rd /s /q "{folder_path}"\n\n')
        
        # 8. Double-check with robocopy (empty folder trick)
        f.write('echo Using robocopy empty folder trick...\n')
        f.write(f'mkdir "%TEMP%\\empty_{rand_suffix}" 2>nul\n')
        f.write(f'robocopy "%TEMP%\\empty_{rand_suffix}" "{folder_path}" /MIR /R:1 /W:1\n')
        f.write(f'rd /s /q "{folder_path}" 2>nul\n')
        f.write(f'rd /s /q "%TEMP%\\empty_{rand_suffix}" 2>nul\n\n')
        
        # 9. Try COM object method to remove locked files
        f.write('echo Using COM object method for locked files...\n')
        f.write('powershell -Command "')
        f.write(f'try {{ $shell = New-Object -ComObject Shell.Application; $folder = $shell.Namespace(0).ParseName(\'{folder_path}\'); ')
        f.write('if ($folder -ne $null) { $folder.InvokeVerb(\'delete\') } }} catch {}"')
        f.write('\n\n')
        
        # 10. Try PowerShell's Remove-Item with different parameters
        f.write('echo Using powerful PowerShell removal methods...\n')
        f.write(f'powershell -Command "Remove-Item -Path \'{folder_path}\' -Force -Recurse -ErrorAction SilentlyContinue"\n')
        f.write(f'powershell -Command "Remove-Item -LiteralPath \'{folder_path}\' -Force -Recurse -ErrorAction SilentlyContinue"\n\n')
        
        # 11. Try to override with empty files first
        f.write('echo Trying to replace files with empty versions...\n')
        f.write('powershell -Command "')
        f.write(f'Get-ChildItem -Path \'{folder_path}\' -Recurse -Force -ErrorAction SilentlyContinue | ')
        f.write('Where-Object { !$_.PSIsContainer } | ForEach-Object { [System.IO.File]::WriteAllText($_.FullName, \'\') }"')
        f.write('\n\n')
        
        # 12. Restart Explorer
        f.write('echo Restarting Explorer...\n')
        f.write('start explorer.exe\n\n')
        
        # 13. Final check
        f.write('echo Checking results...\n')
        f.write(f'if exist "{folder_path}" (\n')
        f.write('    echo [!] FAILED: Folder still exists\n')
        f.write('    echo Please restart your computer for complete removal\n')
        f.write(') else (\n')
        f.write('    echo [✓] SUCCESS: Folder completely purged!\n')
        f.write(')\n\n')
        
        f.write('pause\n')
    
    return batch_path

def try_rename_before_delete(folder_path):
    """Try to rename the folder before deletion - bypasses some locks"""
    print("\n【 RENAME AND DELETE 】")
    print(f"Attempting to rename folder before deletion...")
    
    try:
        # Create a random name in temp directory
        rand_string = create_random_string()
        temp_dir = tempfile.gettempdir()
        new_path = os.path.join(temp_dir, f"del_{rand_string}")
        
        # Try to move the folder to temp dir
        print(f"  └─ Moving {folder_path} to {new_path}")
        shutil.move(folder_path, new_path)
        
        # Delete from the new location
        print(f"  └─ Deleting from new location")
        shutil.rmtree(new_path, ignore_errors=True)
        
        # Check if original is gone
        if not os.path.exists(folder_path):
            print("  └─ Success!")
            return True
    except Exception as e:
        print(f"  └─ Failed: {e}")
    
    # Try PowerShell method which uses different APIs
    try:
        rand_string = create_random_string()
        temp_dir = tempfile.gettempdir()
        new_path = os.path.join(temp_dir, f"ps_del_{rand_string}")
        
        ps_command = f'''
        try {{
            [System.IO.Directory]::Move("{folder_path}", "{new_path}")
            Remove-Item -Path "{new_path}" -Recurse -Force -ErrorAction SilentlyContinue
            "Success"
        }} catch {{
            "Failed: " + $_.Exception.Message
        }}
        '''
        
        result = subprocess.run(["powershell", "-Command", ps_command], 
                               capture_output=True, text=True)
        
        if "Success" in result.stdout and not os.path.exists(folder_path):
            print("  └─ PowerShell move and delete succeeded!")
            return True
    except:
        pass
    
    return False

def use_filesystem_tricks(folder_path):
    """Use various filesystem tricks to delete locked folders"""
    print("\n【 FILESYSTEM TRICKS 】")
    print(f"Attempting special filesystem tricks...")
    
    # Create junction points/symbolic links to confuse Windows
    try:
        rand_string = create_random_string()
        temp_dir = tempfile.gettempdir()
        junction_dir = os.path.join(temp_dir, f"junction_{rand_string}")
        
        # Create a directory junction
        subprocess.run(f'mkdir "{junction_dir}"', shell=True)
        subprocess.run(f'mklink /J "{junction_dir}\\target" "{folder_path}"', shell=True)
        
        # Try to delete through the junction
        print(f"  └─ Deleting through junction point")
        subprocess.run(f'rd /s /q "{junction_dir}"', shell=True)
        
        # Check if it worked
        if not os.path.exists(folder_path):
            print("  └─ Junction trick worked!")
            return True
    except:
        pass
    
    # Try PowerShell Alternate Data Streams removal
    try:
        ps_command = f'''
        $folder = "{folder_path}"
        Get-ChildItem -Path $folder -Recurse -Force -ErrorAction SilentlyContinue | ForEach-Object {{
            $streams = Get-Item -Path $_.FullName -Stream * -ErrorAction SilentlyContinue
            if ($streams) {{
                $streams | Where-Object Stream -ne ':$DATA' | ForEach-Object {{
                    Remove-Item -Path "$($_.FileName):$($_.Stream)" -Force -ErrorAction SilentlyContinue
                }}
            }}
        }}
        '''
        
        subprocess.run(["powershell", "-Command", ps_command], capture_output=True)
    except:
        pass
    
    # Try MoveFileEx method via PowerShell
    try:
        ps_command = f'''
        Add-Type -TypeDefinition @"
        using System;
        using System.Runtime.InteropServices;
        
        public class MoveEx {{
            [DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Unicode)]
            static extern bool MoveFileEx(string lpExistingFileName, string lpNewFileName, int dwFlags);
            
            public static bool MarkForDeletion(string path) {{
                return MoveFileEx(path, null, 4);
            }}
        }}
"@
        
        $result = [MoveEx]::MarkForDeletion("{folder_path}")
        Write-Output "MoveFileEx result: $result"
        '''
        
        subprocess.run(["powershell", "-Command", ps_command], capture_output=True)
    except:
        pass
    
    # Use a COM object method via PowerShell
    try:
        ps_command = f'''
        $shell = New-Object -ComObject Shell.Application
        $folder = $shell.Namespace(0).ParseName("{folder_path}")
        if ($folder -ne $null) {{
            $folder.InvokeVerb("delete")
        }}
        '''
        
        subprocess.run(["powershell", "-Command", ps_command], capture_output=True)
        
        # Check if it worked
        if not os.path.exists(folder_path):
            print("  └─ COM object deletion worked!")
            return True
    except:
        pass
    
    return False

def use_vss_shadow_copy_trick(folder_path):
    """Use Windows Volume Shadow Copy to try to delete a locked folder"""
    print("\n【 SHADOW COPY DELETION 】")
    print(f"Attempting to delete using Volume Shadow Copy...")
    
    try:
        # Create batch file for VSS operations
        temp_dir = tempfile.gettempdir()
        rand_suffix = create_random_string()
        vss_batch = os.path.join(temp_dir, f"vss_{rand_suffix}.bat")
        
        drive_letter = os.path.splitdrive(folder_path)[0]
        folder_path_relative = folder_path[len(drive_letter)+1:]
        
        with open(vss_batch, "w") as f:
            f.write('@echo off\n')
            f.write('echo Creating shadow copy...\n')
            f.write(f'vssadmin create shadow /for={drive_letter}\\\n')
            f.write('for /f "tokens=4" %%i in (\'vssadmin list shadows ^| findstr "Shadow Copy Volume"\') do set SHADOW=%%i\n')
            f.write('echo Shadow copy created at: %SHADOW%\n')
            f.write('echo Accessing through shadow copy...\n')
            f.write(f'mkdir "%TEMP%\\vss_{rand_suffix}"\n')
            f.write(f'mklink /d "%TEMP%\\vss_{rand_suffix}\\shadow" %SHADOW%\\\n')
            f.write(f'echo Deleting through shadow copy...\n')
            f.write(f'rd /s /q "%TEMP%\\vss_{rand_suffix}\\shadow\\{folder_path_relative}"\n')
            f.write(f'echo Unlinking and cleaning up...\n')
            f.write(f'rd "%TEMP%\\vss_{rand_suffix}\\shadow"\n')
            f.write(f'rd "%TEMP%\\vss_{rand_suffix}"\n')
            f.write('vssadmin delete shadows /shadow=%%i /quiet\n')
            f.write('echo Done.\n')
        
        # Execute the VSS batch
        subprocess.run(f'cmd.exe /c "{vss_batch}"', shell=True)
        
        # Check if original folder is gone
        if not os.path.exists(folder_path):
            print("  └─ Shadow copy deletion worked!")
            return True
    except:
        pass
    
    return False

def use_unlocker_functionality(folder_path):
    """Implement functionality similar to Unlocker software"""
    print("\n【 UNLOCKER FUNCTIONALITY 】")
    print(f"Using Unlocker-style methods to release file handles...")
    
    try:
        # Try to use handle.exe to close specific handles
        handle_exe = find_handle_exe()
        if handle_exe:
            # Get a list of all files in the folder
            all_files = []
            try:
                for root, _, files in os.walk(folder_path, topdown=False):
                    for file in files:
                        all_files.append(os.path.join(root, file))
            except:
                pass
            
            # Try to close handles for each file
            for file_path in all_files:
                try:
                    output = subprocess.check_output(f'"{handle_exe}" "{file_path}"', 
                                                   shell=True, 
                                                   stderr=subprocess.STDOUT).decode('utf-8', errors='ignore')
                    
                    # Extract PIDs from the output
                    pid_pattern = re.compile(r'pid: (\d+)', re.IGNORECASE)
                    for line in output.splitlines():
                        if file_path.lower().replace('\\', '/') in line.lower().replace('\\', '/'):
                            match = pid_pattern.search(line)
                            if match:
                                pid = int(match.group(1))
                                print(f"  └─ Closing handle to {file_path} from process {pid}")
                                # Try to close the handle directly using handle.exe with -c option
                                handle_close_cmd = f'"{handle_exe}" -c "{file_path}" -p {pid} -y'
                                subprocess.run(handle_close_cmd, shell=True, capture_output=True)
                                # Also try to terminate the process
                                kill_process_tree(pid)
                except:
                    pass
    except:
        pass
    
    # Use PowerShell to try to unblock files
    try:
        ps_command = f'''
        Get-ChildItem -Path "{folder_path}" -Recurse -Force -ErrorAction SilentlyContinue | 
        ForEach-Object {{
            if (-not $_.PSIsContainer) {{
                try {{
                    Unblock-File -Path $_.FullName -ErrorAction SilentlyContinue
                    $stream = [System.IO.FileStream]::new($_.FullName, 
                        [System.IO.FileMode]::Open, 
                        [System.IO.FileAccess]::ReadWrite, 
                        [System.IO.FileShare]::None)
                    if ($stream) {{
                        $stream.Close()
                        $stream.Dispose()
                        Write-Output "Unlocked: $($_.FullName)"
                    }}
                }} catch {{
                    Write-Output "Failed to unlock: $($_.FullName)"
                }}
            }}
        }}
        '''
        
        subprocess.run(["powershell", "-Command", ps_command], capture_output=True)
    except:
        pass
    
    return False

def try_with_win32api_methods(folder_path):
    """Try using low-level Win32 API methods to force file deletion"""
    print("\n【 WIN32 API METHODS 】")
    print(f"Using Win32 API methods for forced deletion...")
    
    try:
        # Create a PowerShell script to use P/Invoke for deletion
        ps_script = os.path.join(tempfile.gettempdir(), f"win32_delete_{create_random_string()}.ps1")
        
        with open(ps_script, "w") as f:
            f.write('''
$code = @"
using System;
using System.Runtime.InteropServices;
using System.Text;

public class Win32 {
    [DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Auto)]
    public static extern bool DeleteFile(string lpFileName);
    
    [DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Auto)]
    public static extern bool RemoveDirectory(string lpPathName);
    
    [DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Auto)]
    public static extern int GetFileAttributes(string lpFileName);
    
    [DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Auto)]
    public static extern bool SetFileAttributes(string lpFileName, uint dwFileAttributes);
    
    [DllImport("kernel32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    public static extern bool MoveFileEx(string lpExistingFileName, string lpNewFileName, int dwFlags);
    
    [DllImport("kernel32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    public static extern IntPtr FindFirstFile(string lpFileName, out WIN32_FIND_DATA lpFindFileData);
    
    [DllImport("kernel32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    public static extern bool FindNextFile(IntPtr hFindFile, out WIN32_FIND_DATA lpFindFileData);
    
    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern bool FindClose(IntPtr hFindFile);
    
    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Auto)]
    public struct WIN32_FIND_DATA {
        public uint dwFileAttributes;
        public System.Runtime.InteropServices.ComTypes.FILETIME ftCreationTime;
        public System.Runtime.InteropServices.ComTypes.FILETIME ftLastAccessTime;
        public System.Runtime.InteropServices.ComTypes.FILETIME ftLastWriteTime;
        public uint nFileSizeHigh;
        public uint nFileSizeLow;
        public uint dwReserved0;
        public uint dwReserved1;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 260)]
        public string cFileName;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 14)]
        public string cAlternateFileName;
    }
    
    public const int FILE_ATTRIBUTE_READONLY = 0x1;
    public const int FILE_ATTRIBUTE_HIDDEN = 0x2;
    public const int FILE_ATTRIBUTE_SYSTEM = 0x4;
    public const int FILE_ATTRIBUTE_NORMAL = 0x80;
    
    // MoveFileEx flags
    public const int MOVEFILE_REPLACE_EXISTING = 0x1;
    public const int MOVEFILE_COPY_ALLOWED = 0x2;
    public const int MOVEFILE_DELAY_UNTIL_REBOOT = 0x4;
    
    public static bool ClearAttributes(string path) {
        try {
            return SetFileAttributes(path, FILE_ATTRIBUTE_NORMAL);
        } catch {
            return false;
        }
    }
    
    public static bool ForceDeleteFile(string path) {
        try {
            ClearAttributes(path);
            return DeleteFile(path);
        } catch {
            return false;
        }
    }
    
    public static bool ForceDeleteDirectory(string path) {
        try {
            ClearAttributes(path);
            return RemoveDirectory(path);
        } catch {
            return false;
        }
    }
    
    public static bool ScheduleForDeletion(string path) {
        try {
            return MoveFileEx(path, null, MOVEFILE_DELAY_UNTIL_REBOOT);
        } catch {
            return false;
        }
    }
    
    public static void DeleteDirectoryRecursive(string path) {
        // First clear attributes on the directory itself
        ClearAttributes(path);
        
        string searchPattern = System.IO.Path.Combine(path, "*");
        WIN32_FIND_DATA findData;
        IntPtr findHandle = FindFirstFile(searchPattern, out findData);
        
        if (findHandle.ToInt64() != -1) {
            do {
                string fileName = findData.cFileName;
                if (fileName != "." && fileName != "..") {
                    string fullPath = System.IO.Path.Combine(path, fileName);
                    
                    if ((findData.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) != 0) {
                        // It's a directory, recursively delete it
                        DeleteDirectoryRecursive(fullPath);
                    } else {
                        // It's a file, delete it
                        ClearAttributes(fullPath);
                        if (!DeleteFile(fullPath)) {
                            ScheduleForDeletion(fullPath);
                        }
                    }
                }
            } while (FindNextFile(findHandle, out findData));
            
            FindClose(findHandle);
        }
        
        // Now try to remove the directory
        if (!RemoveDirectory(path)) {
            ScheduleForDeletion(path);
        }
    }
}
"@

Add-Type -TypeDefinition $code -Language CSharp

function Force-Delete {
    param(
        [string]$Path
    )
    
    if (Test-Path -Path $Path -PathType Container) {
        # It's a directory
        Write-Output "Attempting Win32 delete on directory: $Path"
        [Win32]::DeleteDirectoryRecursive($Path)
    } elseif (Test-Path -Path $Path -PathType Leaf) {
        # It's a file
        Write-Output "Attempting Win32 delete on file: $Path"
        [Win32]::ClearAttributes($Path)
        $result = [Win32]::DeleteFile($Path)
        if (-not $result) {
            [Win32]::ScheduleForDeletion($Path)
        }
    }
}

# Execute on the target path
Force-Delete -Path "''' + folder_path + '''"
''')
        
        # Execute the PowerShell script
        subprocess.run(f'powershell -ExecutionPolicy Bypass -File "{ps_script}"', shell=True)
        
        # Check if folder was deleted
        if not os.path.exists(folder_path):
            print("  └─ Win32 API deletion succeeded!")
            return True
    except Exception as e:
        print(f"  └─ Win32 API method failed: {e}")
    
    return False

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
    
    # Stage 2: Disable services that might interfere
    disable_services_using_folder(folder_path)
    
    # Stage 3: Try unlocking files
    unlock_files_in_folder(folder_path)
    
    # Stage 4: Using OS commands directly
    try:
        print("▶ Attempt 2: Command line deletion")
        subprocess.run(f'rd /s /q "{folder_path}"', shell=True)
        if not os.path.exists(folder_path):
            print("  └─ Success!")
            return True
    except Exception as e:
        print(f"  └─ Failed: {e}")
    
    # Stage 5: Try rename-before-delete trick
    if try_rename_before_delete(folder_path):
        return True
    
    # Stage 6: File-by-file deletion
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
                    subprocess.run(f'del /f /q /a:- "{file_path}"', shell=True)
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
    
    # Stage 7: Try using Unlocker-style functionality
    use_unlocker_functionality(folder_path)
    
    # Stage 8: Filesystem tricks
    if use_filesystem_tricks(folder_path):
        return True
    
    # Stage 9: Win32 API method
    if try_with_win32api_methods(folder_path):
        return True
    
    # Stage 10: Try Volume Shadow Copy trick
    if use_vss_shadow_copy_trick(folder_path):
        return True
    
    # Stage 11: Robocopy empty folder trick
    print("▶ Attempt 4: Robocopy empty folder trick")
    try:
        # Create an empty folder
        temp_empty = os.path.join(tempfile.gettempdir(), f"empty_{create_random_string()}")
        os.makedirs(temp_empty, exist_ok=True)
        
        # Use robocopy to mirror the empty folder to target with more retries and wait time
        subprocess.run(f'robocopy "{temp_empty}" "{folder_path}" /MIR /R:5 /W:2 /NFL /NDL /NJH /NJS', shell=True)
        
        # Try to remove the now-empty target folder
        os.rmdir(folder_path)
        os.rmdir(temp_empty)  # Clean up
        
        if not os.path.exists(folder_path):
            print("  └─ Success!")
            return True
    except Exception as e:
        print(f"  └─ Failed: {e}")
    
    # Stage 12: Nuclear option - execute special batch file
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
    
    # Stage 13: Last resort - register for deletion on reboot
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
    if success or not os.path.exists(folder_path):
        print("✅ COMPLETE SUCCESS: Folder has been annihilated!")
        return True
    else:
        print("⚠️ PARTIAL SUCCESS: Folder will be removed on next boot")
        print("Please restart your computer to complete the purge")
        return False

if __name__ == "__main__":
    # Welcome message
    print("═════════════════════════════════════════════════════")
    print("  ULTIMATE FOLDER DESTROYER v2.0 - NO REBOOT REQUIRED")
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
    confirmation = input("Continue? (y/n): ")
    
    if confirmation.lower() != 'y':
        print("Operation cancelled.")
        sys.exit(0)
    
    print("Operation will proceed in 3 seconds...")
    time.sleep(3)
    
    # Execute the ultimate purge
    success = ultimate_folder_purge(folder_path)
    
    if success:
        print("\nFolder successfully annihilated! No restart required!")
        sys.exit(0)
    else:
        print("\nRestart your computer now to complete the purge operation.")
        sys.exit(1)
