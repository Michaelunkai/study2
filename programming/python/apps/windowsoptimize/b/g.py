import dearpygui.dearpygui as dpg
import os
import subprocess
import sys
import psutil
import tempfile
from pathlib import Path
import time
import ctypes
import traceback
import threading  # Add threading support for concurrent execution

# Global variable to track launched processes
launched_processes = []

# Check for admin privileges
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Function to run as admin
def run_as_admin(command):
    if is_admin():
        return subprocess.Popen(command, shell=True)
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

# For handling shortcuts in Windows
try:
    import win32com.client
    
    def get_target_path(shortcut_path):
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        return shortcut.Targetpath
except ImportError:
    print("Warning: pywin32 not installed. Shortcut resolution may not work properly.")
    
    def get_target_path(shortcut_path):
        return shortcut_path  # Just return the shortcut itself if we can't resolve

def run_tools_callback():
    global launched_processes
    folder_path = r"C:\Users\micha\Desktop\cleanup"
    status_text = "Launching tools...\n"
    
    # Scan the directory for shortcuts and executables
    shortcuts_and_exes = []
    
    try:
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if file.lower().endswith(".lnk"):
                try:
                    target_path = get_target_path(file_path)
                    shortcuts_and_exes.append((file, target_path))
                    status_text += f"Found shortcut: {file} -> {target_path}\n"
                except Exception as e:
                    status_text += f"Failed to resolve shortcut: {file}, Error: {e}\n"
            elif file.lower().endswith(".exe"):
                shortcuts_and_exes.append((file, file_path))
                status_text += f"Found executable: {file}\n"
    except Exception as e:
        status_text += f"Error scanning folder: {e}\n"
    
    # Update status
    dpg.set_value("status_text", status_text)
    
    # Launch each tool
    launched_processes.clear()  # Clear previous processes
    for name, tool_path in shortcuts_and_exes:
        try:
            process = subprocess.Popen(tool_path)
            launched_processes.append((name, process))
            status_text += f"Launched: {name} (PID: {process.pid})\n"
        except Exception as e:
            status_text += f"Failed to launch {name}: {e}\n"
    
    # Final update to status
    dpg.set_value("status_text", status_text)

def get_tool_executable_names():
    """Get all executable names from the cleanup folder including both .exe files and shortcut targets."""
    folder_path = r"C:\Users\micha\Desktop\cleanup"
    executable_names = set()
    
    try:
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if file.lower().endswith(".lnk"):
                try:
                    target_path = get_target_path(file_path)
                    executable_names.add(os.path.basename(target_path).lower())
                except Exception:
                    pass
            elif file.lower().endswith(".exe"):
                executable_names.add(file.lower())
    except Exception:
        pass
        
    return executable_names

def kill_ccleaner():
    """Specifically target and kill CCleaner processes"""
    ccleaner_process_names = [
        "ccleaner.exe", 
        "ccleaner64.exe", 
        "ccleanerslim.exe", 
        "ccleaneragent.exe",
        "ccupdate.exe",
        "ccleanermonitoring.exe"
    ]
    
    killed = False
    status_text = ""
    
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            proc_info = proc.info
            proc_name = proc_info['name'].lower() if proc_info['name'] else ""
            
            if proc_name in ccleaner_process_names:
                try:
                    # Get process
                    p = psutil.Process(proc.pid)
                    
                    # Kill children first
                    for child in p.children(recursive=True):
                        try:
                            child.kill()
                            status_text += f"Killed CCleaner child process: {child.name()} (PID: {child.pid})\n"
                        except:
                            pass
                    
                    # Kill main process
                    p.kill()
                    status_text += f"Force killed CCleaner process: {proc_name} (PID: {proc.pid})\n"
                    killed = True
                except Exception as e:
                    status_text += f"Failed to kill CCleaner process {proc_name} (PID: {proc.pid}): {e}\n"
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    if not killed:
        status_text += "No CCleaner processes found.\n"
    
    return status_text, killed

def close_tools_callback():
    global launched_processes
    status_text = "Closing tools...\n"
    closed_count = 0
    
    # First check specifically for CCleaner
    ccleaner_status, ccleaner_killed = kill_ccleaner()
    status_text += ccleaner_status
    if ccleaner_killed:
        closed_count += 1
    
    # Now try closing processes we launched directly
    for name, process in launched_processes:
        try:
            if process.poll() is None:  # Check if process is still running
                process.terminate()
                try:
                    process.wait(timeout=2)  # Wait for process to terminate
                except subprocess.TimeoutExpired:
                    process.kill()  # Force kill if not responding
                status_text += f"Closed launched process: {name} (PID: {process.pid})\n"
                closed_count += 1
        except Exception as e:
            status_text += f"Failed to close launched process {name}: {e}\n"
    
    # Next, find all running processes that match our tool names
    tool_executables = get_tool_executable_names()
    if tool_executables:
        status_text += f"Looking for processes matching: {', '.join(tool_executables)}\n"
    
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            proc_info = proc.info
            proc_name = proc_info['name'].lower() if proc_info['name'] else ""
            proc_exe = os.path.basename(proc_info['exe']).lower() if proc_info['exe'] else ""
            
            # Check if this process matches any of our tool executables
            if proc_name in tool_executables or proc_exe in tool_executables:
                try:
                    # Get process
                    p = psutil.Process(proc.pid)
                    
                    # Kill process and its children
                    for child in p.children(recursive=True):
                        try:
                            child.terminate()
                            status_text += f"Terminated child process: {child.name()} (PID: {child.pid})\n"
                            closed_count += 1
                        except:
                            try:
                                child.kill()
                                status_text += f"Killed child process: {child.name()} (PID: {child.pid})\n"
                                closed_count += 1
                            except:
                                pass
                    
                    # Terminate the main process
                    p.terminate()
                    status_text += f"Terminated process: {proc_name} (PID: {proc.pid})\n"
                    closed_count += 1
                    
                    # Give it a moment to terminate
                    time.sleep(0.5)
                    
                    # If still running, kill it forcibly
                    if p.is_running():
                        p.kill()
                        status_text += f"Force killed process: {proc_name} (PID: {proc.pid})\n"
                except Exception as e:
                    status_text += f"Failed to terminate process {proc_name} (PID: {proc.pid}): {e}\n"
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    if closed_count == 0:
        status_text += "No matching processes found to close.\n"
    else:
        status_text += f"Successfully closed {closed_count} processes.\n"
    
    # Clear our process tracking list
    launched_processes.clear()
    dpg.set_value("status_text", status_text)

def run_powershell_with_realtime_output(command, status_text, temp_file_path=None):
    """Execute a PowerShell command and show real-time output in the status area"""
    try:
        # Start the process with pipe for stdout and stderr
        process = subprocess.Popen(
            command, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            bufsize=1,  # Line buffered
            universal_newlines=True,  # Text mode
            encoding='utf-8',
            errors='replace'  # Replace invalid characters
        )
        
        # Create threads to read stdout and stderr in real-time
        def read_output(pipe, is_error=False):
            prefix = "ERROR: " if is_error else ""
            for line in iter(pipe.readline, ''):
                if line:
                    # Update UI with each new line of output
                    nonlocal status_text
                    status_text += f"{prefix}{line}"
                    dpg.set_value("status_text", status_text)
        
        # Start threads for reading stdout and stderr
        stdout_thread = threading.Thread(target=read_output, args=(process.stdout,), daemon=True)
        stderr_thread = threading.Thread(target=read_output, args=(process.stderr, True), daemon=True)
        stdout_thread.start()
        stderr_thread.start()
        
        # Wait for the process to complete
        while process.poll() is None:
            time.sleep(0.1)  # Small sleep to reduce CPU usage
            dpg.set_value("status_text", status_text)
        
        # Wait for output threads to finish
        stdout_thread.join(timeout=1)
        stderr_thread.join(timeout=1)
        
        # Cleanup temporary file if provided
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
                status_text += "Temporary script file cleaned up.\n"
            except:
                status_text += "Could not delete temporary script file.\n"
        
        # Add final status based on return code
        if process.returncode == 0:
            status_text += "Command completed successfully!\n"
        else:
            status_text += f"Command exited with code {process.returncode}.\n"
        
        return status_text, process.returncode
        
    except Exception as e:
        status_text += f"Error executing command: {str(e)}\n"
        status_text += traceback.format_exc() + "\n"
        return status_text, -1

def run_ps1_clean_callback():
    """Execute the PowerShell clean function"""
    status_text = "Starting PowerShell system cleanup...\n"
    dpg.set_value("status_text", status_text)
    
    # Create the PowerShell script content - Added 'r' prefix to make it a raw string
    ps1_script = r'''
function clean {
    Write-Host "Starting deep system cleanup..." -ForegroundColor Cyan

    # Try to run the custom commands, but don't fail if they don't exist
    try { ws 'rmp' } catch { Write-Host "ws command not found, skipping" }
    try { cctemp } catch { Write-Host "cctemp command not found, skipping" }
    
    Write-Host "Cleaning temporary files..." -ForegroundColor Green
    Remove-Item -Path $env:TEMP\*, "$env:WINDIR\Temp\*", "$env:WINDIR\Prefetch\*", "C:\Users\*\AppData\Local\Temp\*" -Force -Recurse -ErrorAction SilentlyContinue
    
    Write-Host "Running Disk Cleanup utility..." -ForegroundColor Green
    try { cleanmgr /sageset:1 } catch { Write-Host "cleanmgr setup failed, continuing..." }
    try { cleanmgr /sagerun:1 } catch { Write-Host "cleanmgr run failed, continuing..." }
    try { cleanmgr /lowdisk } catch { Write-Host "cleanmgr lowdisk failed, continuing..." }
    
    # Clear recycle bin
    Write-Host "Clearing recycle bin..." -ForegroundColor Green
    try {
        PowerShell -Command "Clear-RecycleBin -Force"
        Write-Host "Recycle bin cleared successfully." -ForegroundColor Yellow
    } catch {
        Write-Host "Could not clear recycle bin, continuing..." -ForegroundColor Yellow
    }

    # System health checks
    try {
        Write-Host "Running system health checks..." -ForegroundColor Cyan
        Write-Host "Running Repair-WindowsImage -Online -ScanHealth..." -ForegroundColor Yellow
        Repair-WindowsImage -Online -ScanHealth
        
        Write-Host "Running Repair-WindowsImage -Online -RestoreHealth..." -ForegroundColor Yellow
        Repair-WindowsImage -Online -RestoreHealth
        
        Write-Host "Running sfc /scannow - this may take several minutes..." -ForegroundColor Yellow
        sfc /scannow
        
        Write-Host "Running DISM.exe /Online /Cleanup-Image /CheckHealth..." -ForegroundColor Yellow
        DISM.exe /Online /Cleanup-Image /CheckHealth
        
        Write-Host "Running DISM.exe /Online /Cleanup-Image /RestoreHealth..." -ForegroundColor Yellow
        DISM.exe /Online /Cleanup-Image /RestoreHealth
        
        Write-Host "Running dism /online /cleanup-image /startcomponentcleanup..." -ForegroundColor Yellow
        dism /online /cleanup-image /startcomponentcleanup
        
        Write-Host "Running dism /online /Cleanup-Image /AnalyzeComponentStore..." -ForegroundColor Yellow
        dism /online /Cleanup-Image /AnalyzeComponentStore
        
        Write-Host "Running dism /online /Cleanup-Image /StartComponentCleanup /ResetBase..." -ForegroundColor Yellow
        dism /online /Cleanup-Image /StartComponentCleanup /ResetBase
        
        Write-Host "System health checks completed." -ForegroundColor Green
    } catch {
        Write-Host "Some system health checks failed, continuing..." -ForegroundColor Yellow
    }

    # Network reset
    try {
        Write-Host "Resetting network components..." -ForegroundColor Cyan
        Write-Host "Running netsh int ip reset..." -ForegroundColor Yellow
        netsh int ip reset
        
        Write-Host "Running ipconfig /release..." -ForegroundColor Yellow
        ipconfig /release
        
        Write-Host "Running ipconfig /renew..." -ForegroundColor Yellow
        ipconfig /renew
        
        Write-Host "Running netsh winsock reset..." -ForegroundColor Yellow
        netsh winsock reset
        
        Write-Host "Running ipconfig /flushdns..." -ForegroundColor Yellow
        ipconfig /flushdns
        
        Write-Host "Network components reset successfully." -ForegroundColor Green
    } catch {
        Write-Host "Network reset had issues, continuing..." -ForegroundColor Yellow
    }

    # Windows Update
    try {
        Write-Host "Working with Windows Updates..." -ForegroundColor Cyan
        Write-Host "Starting wuauserv service..." -ForegroundColor Yellow
        net start wuauserv
        
        # Only try to install module if it doesn't exist
        Write-Host "Checking for PSWindowsUpdate module..." -ForegroundColor Yellow
        if (-not (Get-Module -ListAvailable -Name PSWindowsUpdate)) {
            Write-Host "Installing PSWindowsUpdate module..." -ForegroundColor Yellow
            Install-Module -Name PSWindowsUpdate -Force -AllowClobber -Scope CurrentUser
        }
        
        Write-Host "Running Get-WindowsUpdate -Install -AcceptAll..." -ForegroundColor Yellow
        Get-WindowsUpdate -Install -AcceptAll -Verbose
        
        Write-Host "Cleaning up Windows Update download cache..." -ForegroundColor Yellow
        Remove-Item -Path "C:\Windows\SoftwareDistribution\Download\*" -Force -Recurse -ErrorAction SilentlyContinue
        
        Write-Host "Windows Update operations completed." -ForegroundColor Green
    } catch {
        Write-Host "Windows Update operations had issues, continuing..." -ForegroundColor Yellow
    }

    # Disk optimization
    try {
        Write-Host "Optimizing disk..." -ForegroundColor Cyan
        Write-Host "Running defrag C: /U /V..." -ForegroundColor Yellow
        defrag C: /U /V
        
        Write-Host "Running defrag /c /o..." -ForegroundColor Yellow
        defrag /c /o
        
        Write-Host "Running Optimize-Volume -DriveLetter C -ReTrim..." -ForegroundColor Yellow
        Optimize-Volume -DriveLetter C -ReTrim -Confirm:$false -Verbose
        
        Write-Host "Setting fsutil memory usage..." -ForegroundColor Yellow
        fsutil behavior set memoryusage 2
        
        Write-Host "Running compact.exe /CompactOS:always..." -ForegroundColor Yellow
        compact.exe /CompactOS:always
        
        Write-Host "Disk optimization completed." -ForegroundColor Green
    } catch {
        Write-Host "Some disk optimization operations failed, continuing..." -ForegroundColor Yellow
    }

    # Volume shadow copy cleanup
    try {
        Write-Host "Cleaning up volume shadow copies..." -ForegroundColor Cyan
        vssadmin delete shadows /for=C: /all /quiet
        vssadmin delete shadows /for=C: /oldest
        Write-Host "Volume shadow copy cleanup completed." -ForegroundColor Green
    } catch {
        Write-Host "Shadow copy cleanup had issues, continuing..." -ForegroundColor Yellow
    }

    # Run silent cleanup
    try {
        Write-Host "Running silent cleanup task..." -ForegroundColor Cyan
        schtasks /Run /TN "\Microsoft\Windows\DiskCleanup\SilentCleanup"
        Write-Host "Silent cleanup task executed." -ForegroundColor Green
    } catch {
        Write-Host "Silent cleanup failed, continuing..." -ForegroundColor Yellow
    }

    # Event log clearing
    try {
        Write-Host "Clearing event logs..." -ForegroundColor Cyan
        wevtutil cl Application
        wevtutil cl Security
        wevtutil cl System
        wevtutil cl Setup
        wevtutil cl ForwardedEvents
        Write-Host "Event logs cleared." -ForegroundColor Green
    } catch {
        Write-Host "Event log clearing had issues, continuing..." -ForegroundColor Yellow
    }

    # File cleanups
    Write-Host "Cleaning system files..." -ForegroundColor Cyan
    Write-Host "Cleaning Windows CBS logs..." -ForegroundColor Yellow
    del /q/f/s "C:\Windows\Logs\CBS\*"
    
    Write-Host "Cleaning Windows DISM logs..." -ForegroundColor Yellow
    del /q/f/s "C:\Windows\Logs\DISM\*"
    
    Write-Host "Cleaning Windows Update logs..." -ForegroundColor Yellow
    del /q/f/s "C:\Windows\Logs\WindowsUpdate\*"
    
    Write-Host "Cleaning Windows Prefetch..." -ForegroundColor Yellow
    del /q/f/s "C:\Windows\Prefetch\*"
    
    Write-Host "Cleaning Explorer thumbcache..." -ForegroundColor Yellow
    del /f /s /q "$env:LocalAppData\Microsoft\Windows\Explorer\thumbcache_*"
    
    Write-Host "Cleaning Windows Error Reporting files..." -ForegroundColor Yellow
    del /q/f/s "C:\ProgramData\Microsoft\Windows\WER\*"
    
    Write-Host "Cleaning Temporary Internet Files..." -ForegroundColor Yellow
    del /q/f/s "$env:USERPROFILE\AppData\Local\Microsoft\Windows\Temporary Internet Files\*"
    
    Write-Host "Cleaning WMI logs..." -ForegroundColor Yellow
    del /q/f/s "C:\Windows\Logs\WMI\*.log"
    
    Write-Host "Cleaning Delivery Optimization files..." -ForegroundColor Yellow
    del /q/f/s "C:\Windows\SoftwareDistribution\DeliveryOptimization\*"
    
    Write-Host "Cleaning Edge browser cache..." -ForegroundColor Yellow
    del /q/f/s "$env:USERPROFILE\AppData\Local\Microsoft\Edge\User Data\Default\Cache\*"
    
    Write-Host "Cleaning Edge browser downloads..." -ForegroundColor Yellow
    del /q/f/s "$env:USERPROFILE\AppData\Local\Microsoft\Edge\User Data\Default\Downloads\*"
    
    Write-Host "Cleaning Windows Defender scan history..." -ForegroundColor Yellow
    del /q/f/s "C:\ProgramData\Microsoft\Windows Defender\Scans\History\*"
    
    Write-Host "Cleaning OneDrive logs..." -ForegroundColor Yellow
    del /q/f/s "$env:USERPROFILE\AppData\Local\Microsoft\OneDrive\logs\*"
    
    Write-Host "Cleaning Office file cache..." -ForegroundColor Yellow
    del /q/f/s "$env:USERPROFILE\AppData\Local\Microsoft\Office\16.0\OfficeFileCache\*"
    
    Write-Host "Cleaning Windows Error Reporting queue..." -ForegroundColor Yellow
    del /q/f/s "C:\ProgramData\Microsoft\Windows\WER\ReportQueue\*"
    
    Write-Host "File cleanups completed." -ForegroundColor Green

    # Windows Store repair
    try {
        Write-Host "Repairing Windows Store..." -ForegroundColor Cyan
        Get-AppxPackage -allusers Microsoft.WindowsStore | ForEach-Object {
            Add-AppxPackage -register "$($_.InstallLocation)\appxmanifest.xml" -DisableDevelopmentMode
        }
        Write-Host "Windows Store repair completed." -ForegroundColor Green
    } catch {
        Write-Host "Windows Store repair failed, continuing..." -ForegroundColor Yellow
    }

    # Additional cleanups
    Write-Host "Performing additional cleanups..." -ForegroundColor Cyan
    Write-Host "Cleaning Windows Installer patch cache..." -ForegroundColor Yellow
    Remove-Item -Path "C:\Windows\Installer\$PatchCache$\*" -Force -Recurse -ErrorAction SilentlyContinue
    
    Write-Host "Cleaning old files from Windows Temp..." -ForegroundColor Yellow
    forfiles /p "C:\Windows\Temp" /s /m *.* /d -7 /c "cmd /c del @path" 2>$null
    
    Write-Host "Additional cleanups completed." -ForegroundColor Green

    # Network optimizations
    try {
        Write-Host "Optimizing network settings..." -ForegroundColor Cyan
        Write-Host "Setting TCP autotuninglevel to normal..." -ForegroundColor Yellow
        netsh int tcp set global autotuninglevel=normal
        
        Write-Host "Setting TCP autotuninglevel to highlyrestricted..." -ForegroundColor Yellow
        netsh int tcp set global autotuninglevel=highlyrestricted
        
        Write-Host "Enabling TCP DCA..." -ForegroundColor Yellow
        netsh int tcp set global dca=enabled
        
        Write-Host "Enabling TCP ECN capability..." -ForegroundColor Yellow
        netsh int tcp set global ecncapability=enabled
        
        Write-Host "Network optimizations completed." -ForegroundColor Green
    } catch {
        Write-Host "Network optimization had issues, continuing..." -ForegroundColor Yellow
    }

    Write-Host "System cleanup completed!" -ForegroundColor Green
}

# Execute the clean function
clean
'''
    
    try:
        # Create a temporary PS1 file
        with tempfile.NamedTemporaryFile(suffix='.ps1', delete=False) as temp_file:
            temp_file_path = temp_file.name
            temp_file.write(ps1_script.encode('utf-8'))
        
        status_text += f"Created temporary script at: {temp_file_path}\n"
        
        # Execute PowerShell with elevated privileges
        if is_admin():
            # We're already admin, run directly with real-time output
            command = f'powershell.exe -ExecutionPolicy Bypass -File "{temp_file_path}"'
            status_text += f"Running command as admin: {command}\n"
            dpg.set_value("status_text", status_text)
            
            # Use the real-time output function
            status_text, returncode = run_powershell_with_realtime_output(command, status_text, temp_file_path)
            
        else:
            # Need to elevate - save info about what we're trying to do
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "run_ps_clean.flag"), "w") as flag_file:
                flag_file.write(temp_file_path)
                
            status_text += "Requesting administrator privileges to run cleanup...\n"
            dpg.set_value("status_text", status_text)
            
            # Relaunch as admin
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{os.path.abspath(__file__)}" --ps-clean-admin', None, 1)
            status_text += "Cleanup process launched with admin rights in a new window.\n"
            
    except Exception as e:
        status_text += f"Error executing PowerShell cleanup: {str(e)}\n"
        status_text += traceback.format_exc() + "\n"
    
    # Update final status
    dpg.set_value("status_text", status_text)

def qaccess_callback():
    """Execute the qaccess PowerShell function to pin folders to Quick Access"""
    status_text = "Setting up Quick Access pins...\n"
    dpg.set_value("status_text", status_text)
    
    # Create the PowerShell script content with updated function
    ps1_script = r'''
function qaccess {
    # Remove all QuickAccess pinned items.
    # Removing every file in AutomaticDestinations will clear QuickAccess.
    Remove-Item "$env:APPDATA\Microsoft\Windows\Recent\AutomaticDestinations\*" -Force -Recurse
    Start-Sleep -Seconds 1

    # Define the list of folders that we want to add to QuickAccess.
    $folders = @(
        "F:\backup\windowsapps",
        "F:\backup\windowsapps\installed",
        "F:\backup\windowsapps\install",
        "F:\backup\windowsapps\profile",
        "C:\Users\micha\Videos",
        "C:\games",
        "F:\study",
        "F:\backup",
        "C:\Users\micha"
    )

    # Create a Shell.Application COM object for pinning folders.
    $shell = New-Object -ComObject Shell.Application

    foreach ($folder in $folders) {
        # If the folder is on the C: drive but is not an exception (does not contain "micha" and isn't exactly "C:\games"), change its drive to F:
        if ($folder -like "C:\*") {
            if (($folder -notlike "*micha*") -and ($folder -ne "C:\games")) {
                $folder = $folder -replace "^C:", "F:"
            }
        }
        
        # Attempt to get the folder namespace. If found, pin it to QuickAccess.
        $ns = $shell.Namespace($folder)
        if ($ns) {
            $ns.Self.InvokeVerb("pintohome")
            Write-Host "Pinned to Quick Access: $folder"
        }
        else {
            Write-Host "Folder not found or inaccessible: $folder"
        }
    }
}

# Execute the function
qaccess
'''
    
    try:
        # Create a temporary PS1 file
        with tempfile.NamedTemporaryFile(suffix='.ps1', delete=False) as temp_file:
            temp_file_path = temp_file.name
            temp_file.write(ps1_script.encode('utf-8'))
        
        status_text += f"Created temporary script at: {temp_file_path}\n"
        
        # Execute PowerShell script
        command = f'powershell.exe -ExecutionPolicy Bypass -File "{temp_file_path}"'
        status_text += f"Running command: {command}\n"
        dpg.set_value("status_text", status_text)
        
        # Run the command
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Update status while waiting
        while process.poll() is None:
            dpg.set_value("status_text", status_text + "Quick Access setup in progress...\n")
            time.sleep(0.5)
        
        # Get output
        stdout, stderr = process.communicate()
        output = stdout.decode('utf-8', errors='ignore')
        error = stderr.decode('utf-8', errors='ignore')
        
        if output:
            status_text += "Output:\n" + output + "\n"
        if error:
            status_text += "Errors:\n" + error + "\n"
            
        if process.returncode == 0:
            status_text += "Quick Access folders pinned successfully!\n"
        else:
            status_text += f"Quick Access setup exited with code {process.returncode}.\n"
            
    except Exception as e:
        status_text += f"Error executing Quick Access setup: {str(e)}\n"
        status_text += traceback.format_exc() + "\n"
    
    finally:
        # Clean up temporary file
        try:
            if 'temp_file_path' in locals():
                os.unlink(temp_file_path)
                status_text += "Temporary script file cleaned up.\n"
        except:
            status_text += "Could not delete temporary script file.\n"
            
        # Update final status
        dpg.set_value("status_text", status_text)

def run_powershell_function(function_name):
    """Execute a specific PowerShell function by name with real-time output"""
    status_text = f"Running PowerShell function: {function_name}...\n"
    dpg.set_value("status_text", status_text)
    
    try:
        # Execute PowerShell with the function name
        command = f'powershell.exe -ExecutionPolicy Bypass -Command "& {{ Write-Host \"Starting {function_name} function...\" -ForegroundColor Cyan; {function_name}; Write-Host \"{function_name} function completed.\" -ForegroundColor Green }}"'
        status_text += f"Running command: {command}\n"
        dpg.set_value("status_text", status_text)
        
        # Use the real-time output function
        status_text, returncode = run_powershell_with_realtime_output(command, status_text)
    except Exception as e:
        status_text += f"Error executing PowerShell function: {str(e)}\n"
        status_text += traceback.format_exc() + "\n"
    
    # Update final status
    dpg.set_value("status_text", status_text)

def run_windows_updates():
    """Execute Windows update check and install with real-time output"""
    status_text = "Starting Windows Updates...\n"
    dpg.set_value("status_text", status_text)
    
    ps_script = r'''
    try {
        Write-Host "Working with Windows Updates..." -ForegroundColor Cyan
        Write-Host "Starting Windows Update service..." -ForegroundColor Yellow
        net start wuauserv
        
        # Only try to install module if it doesn't exist
        Write-Host "Checking for PSWindowsUpdate module..." -ForegroundColor Yellow
        if (-not (Get-Module -ListAvailable -Name PSWindowsUpdate)) {
            Write-Host "Installing PSWindowsUpdate module..." -ForegroundColor Yellow
            Install-Module -Name PSWindowsUpdate -Force -AllowClobber -Scope CurrentUser
        }
        
        Write-Host "Checking for and installing Windows Updates - this may take some time..." -ForegroundColor Yellow
        Get-WindowsUpdate -Install -AcceptAll -Verbose
        
        Write-Host "Windows Updates completed successfully" -ForegroundColor Green
    } catch {
        Write-Host "Windows Update operations had issues: $_" -ForegroundColor Red
    }
    '''
    
    try:
        # Create a temporary PS1 file
        with tempfile.NamedTemporaryFile(suffix='.ps1', delete=False) as temp_file:
            temp_file_path = temp_file.name
            temp_file.write(ps_script.encode('utf-8'))
        
        status_text += f"Created temporary script at: {temp_file_path}\n"
        
        # Execute PowerShell with elevated privileges
        if is_admin():
            # We're already admin, run directly with real-time output
            command = f'powershell.exe -ExecutionPolicy Bypass -File "{temp_file_path}"'
            status_text += f"Running Windows Updates as admin: {command}\n"
            dpg.set_value("status_text", status_text)
            
            # Use the real-time output function
            status_text, returncode = run_powershell_with_realtime_output(command, status_text, temp_file_path)
        else:
            # Need to elevate
            status_text += "Requesting administrator privileges to run Windows Updates...\n"
            dpg.set_value("status_text", status_text)
            
            # Relaunch as admin
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{os.path.abspath(__file__)}" --windows-updates', None, 1)
            status_text += "Windows Updates launched with admin rights in a new window.\n"
            
    except Exception as e:
        status_text += f"Error executing Windows Updates: {str(e)}\n"
        status_text += traceback.format_exc() + "\n"
        dpg.set_value("status_text", status_text)

def clear_temp_files():
    """Purge all temporary files from the system with real-time output"""
    status_text = "Starting temporary file cleanup...\n"
    dpg.set_value("status_text", status_text)
    
    ps_script = r'''
    function Clear-AllTempFiles {
        Write-Host "Starting temp file cleanup..." -ForegroundColor Cyan
        
        # Common temp locations
        $locations = @(
            "$env:TEMP",
            "$env:WINDIR\Temp",
            "$env:WINDIR\Prefetch",
            "C:\Users\*\AppData\Local\Temp",
            "C:\Windows\SoftwareDistribution\Download",
            "C:\ProgramData\Microsoft\Windows\WER\ReportQueue",
            "C:\ProgramData\Microsoft\Windows\WER\ReportArchive",
            "C:\Users\*\AppData\Local\Microsoft\Windows\INetCache",
            "C:\Users\*\AppData\Local\Microsoft\Windows\WER",
            "C:\Users\*\AppData\Local\Microsoft\Terminal Server Client\Cache",
            "C:\Windows\Logs",
            "C:\Windows\Debug",
            "C:\Users\*\AppData\Local\CrashDumps",
            "C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\ThumbCacheToDelete"
        )
        
        foreach ($location in $locations) {
            try {
                if (Test-Path -Path $location) {
                    Write-Host "Cleaning $location" -ForegroundColor Yellow
                    $fileCount = (Get-ChildItem -Path $location -Force -Recurse -ErrorAction SilentlyContinue | Where-Object { $_.PSIsContainer -eq $false }).Count
                    if ($fileCount -gt 0) {
                        Write-Host "Found $fileCount files to clean..." -ForegroundColor Cyan
                        Get-ChildItem -Path $location -Force -Recurse -ErrorAction SilentlyContinue | 
                        Where-Object { $_.PSIsContainer -eq $false } | 
                        ForEach-Object {
                            try {
                                Remove-Item -Path $_.FullName -Force -ErrorAction SilentlyContinue
                                Write-Host "Removed $($_.FullName)" -ForegroundColor DarkGray
                            } catch {
                                Write-Host "Failed to remove $($_.FullName): $_" -ForegroundColor Red
                            }
                        }
                    } else {
                        Write-Host "No files found to clean in $location" -ForegroundColor Green
                    }
                    Write-Host "Completed cleaning $location" -ForegroundColor Green
                }
            } catch {
                Write-Host "Failed to clean $location : $_" -ForegroundColor Red
            }
        }
        
        # Clear browser caches
        $browserPaths = @(
            "C:\Users\*\AppData\Local\Google\Chrome\User Data\Default\Cache",
            "C:\Users\*\AppData\Local\Microsoft\Edge\User Data\Default\Cache",
            "C:\Users\*\AppData\Local\Mozilla\Firefox\Profiles\*\cache2"
        )
        
        foreach ($path in $browserPaths) {
            try {
                if (Test-Path -Path $path) {
                    Write-Host "Cleaning browser cache: $path" -ForegroundColor Yellow
                    $fileCount = (Get-ChildItem -Path "$path\*" -Force -Recurse -ErrorAction SilentlyContinue).Count
                    Write-Host "Found $fileCount browser cache files to clean..." -ForegroundColor Cyan
                    Remove-Item -Path "$path\*" -Force -Recurse -ErrorAction SilentlyContinue
                    Write-Host "Completed cleaning browser cache" -ForegroundColor Green
                }
            } catch {
                Write-Host "Failed to clean browser cache: $_" -ForegroundColor Red
            }
        }
        
        # Clear DNS cache
        Write-Host "Flushing DNS cache..." -ForegroundColor Yellow
        ipconfig /flushdns
        Write-Host "DNS cache flushed" -ForegroundColor Green
        
        Write-Host "Temp file cleanup completed!" -ForegroundColor Green
    }
    
    Clear-AllTempFiles
    '''
    
    try:
        # Create a temporary PS1 file
        with tempfile.NamedTemporaryFile(suffix='.ps1', delete=False) as temp_file:
            temp_file_path = temp_file.name
            temp_file.write(ps_script.encode('utf-8'))
        
        status_text += f"Created temporary script at: {temp_file_path}\n"
        
        # Execute PowerShell with elevated privileges
        if is_admin():
            # We're already admin, run directly with real-time output
            command = f'powershell.exe -ExecutionPolicy Bypass -File "{temp_file_path}"'
            status_text += f"Clearing temp files as admin: {command}\n"
            dpg.set_value("status_text", status_text)
            
            # Use the real-time output function
            status_text, returncode = run_powershell_with_realtime_output(command, status_text, temp_file_path)
        else:
            # Need to elevate
            status_text += "Requesting administrator privileges to clear temp files...\n"
            dpg.set_value("status_text", status_text)
            
            # Relaunch as admin
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{os.path.abspath(__file__)}" --clear-temps', None, 1)
            status_text += "Temp file cleanup launched with admin rights in a new window.\n"
            
    except Exception as e:
        status_text += f"Error executing temp file cleanup: {str(e)}\n"
        status_text += traceback.format_exc() + "\n"
        dpg.set_value("status_text", status_text)

def run_all_cleanup():
    """Run all cleanup operations and nvidia function in sequence"""
    status_text = "Starting all cleanup operations...\n"
    dpg.set_value("status_text", status_text)
    
    # Run tools first
    status_text += "\n=== RUNNING CLEANUP TOOLS ===\n"
    dpg.set_value("status_text", status_text)
    run_tools_callback()
    
    # Get current status and append
    status_text = dpg.get_value("status_text")
    
    # Run PS1 clean
    status_text += "\n=== RUNNING PS1 CLEAN ===\n"
    dpg.set_value("status_text", status_text)
    run_ps1_clean_callback()
    
    # Update status
    status_text = dpg.get_value("status_text")
    
    # Run clear temp files
    status_text += "\n=== CLEARING TEMP FILES ===\n"
    dpg.set_value("status_text", status_text)
    clear_temp_files()
    
    # Update status
    status_text = dpg.get_value("status_text")
    
    # Run Windows updates
    status_text += "\n=== RUNNING WINDOWS UPDATES ===\n"
    dpg.set_value("status_text", status_text)
    run_windows_updates()
    
    # Update status
    status_text = dpg.get_value("status_text")
    
    # Run nvidia PowerShell function
    status_text += "\n=== RUNNING NVIDIA DRIVER UPDATE ===\n"
    dpg.set_value("status_text", status_text)
    run_powershell_function("nvidia")
    
    # Final update
    status_text = dpg.get_value("status_text")
    status_text += "\n=== ALL CLEANUP OPERATIONS COMPLETED ===\n"
    dpg.set_value("status_text", status_text)

def run_malwarebytes_install():
    """Download and install Malwarebytes silently"""
    status_text = "Starting Malwarebytes download and installation...\n"
    dpg.set_value("status_text", status_text)
    
    # Use the exact one-liner as requested
    ps_command = 'Invoke-WebRequest -Uri "https://downloads.malwarebytes.com/file/mb3" -OutFile "$env:TEMP\\mb3-setup.exe"; Start-Process "$env:TEMP\\mb3-setup.exe" -ArgumentList "/quiet" -Wait'
    
    try:
        # Execute PowerShell command
        command = f'powershell.exe -ExecutionPolicy Bypass -Command "{ps_command}"'
        status_text += f"Running command: {command}\n"
        dpg.set_value("status_text", status_text)
        
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Update status while waiting
        while process.poll() is None:
            dpg.set_value("status_text", status_text + "Downloading and installing Malwarebytes...\n")
            time.sleep(1)
        
        # Get output
        stdout, stderr = process.communicate()
        output = stdout.decode('utf-8', errors='ignore')
        error = stderr.decode('utf-8', errors='ignore')
        
        if output:
            status_text += "Output:\n" + output + "\n"
        if error:
            status_text += "Errors:\n" + error + "\n"
            
        if process.returncode == 0:
            status_text += "Malwarebytes installation completed successfully!\n"
        else:
            status_text += f"Malwarebytes installation exited with code {process.returncode}.\n"
            
    except Exception as e:
        status_text += f"Error installing Malwarebytes: {str(e)}\n"
        status_text += traceback.format_exc() + "\n"
    
    # Update final status
    dpg.set_value("status_text", status_text)

def run_kvrt():
    """Launch the Kaspersky Virus Removal Tool"""
    status_text = "Launching Kaspersky Virus Removal Tool...\n"
    dpg.set_value("status_text", status_text)
    
    kvrt_path = r"F:\backup\windowsapps\installed\KVRT\KVRT.exe"
    
    try:
        if os.path.exists(kvrt_path):
            process = subprocess.Popen(kvrt_path)
            status_text += f"KVRT launched successfully (PID: {process.pid}).\n"
        else:
            status_text += f"Error: KVRT not found at path: {kvrt_path}\n"
    except Exception as e:
        status_text += f"Error launching KVRT: {str(e)}\n"
        status_text += traceback.format_exc() + "\n"
    
    # Update status
    dpg.set_value("status_text", status_text)

def run_powershell_script(script_path):
    """Execute a specific PowerShell script file"""
    status_text = f"Running PowerShell script: {script_path}...\n"
    dpg.set_value("status_text", status_text)
    
    try:
        # Check if file exists
        if not os.path.exists(script_path):
            status_text += f"Error: Script file not found at: {script_path}\n"
            dpg.set_value("status_text", status_text)
            return
            
        # Execute PowerShell script
        command = f'powershell.exe -ExecutionPolicy Bypass -File "{script_path}"'
        status_text += f"Running command: {command}\n"
        dpg.set_value("status_text", status_text)
        
        # Run the command
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Update status while waiting
        while process.poll() is None:
            dpg.set_value("status_text", status_text + f"Script execution in progress...\n")
            time.sleep(0.5)
        
        # Get output
        stdout, stderr = process.communicate()
        output = stdout.decode('utf-8', errors='ignore')
        error = stderr.decode('utf-8', errors='ignore')
        
        if output:
            status_text += "Output:\n" + output + "\n"
        if error:
            status_text += "Errors:\n" + error + "\n"
            
        if process.returncode == 0:
            status_text += f"PowerShell script executed successfully!\n"
        else:
            status_text += f"PowerShell script exited with code {process.returncode}.\n"
            
    except Exception as e:
        status_text += f"Error executing PowerShell script: {str(e)}\n"
        status_text += traceback.format_exc() + "\n"
    
    # Update final status
    dpg.set_value("status_text", status_text)

def run_all_after_format():
    """Run all PowerShell functions from the After Format tab"""
    status_text = "Running all After Format functions...\n"
    dpg.set_value("status_text", status_text)
    
    # List of all PowerShell functions in the After Format tab
    ps_functions = [
        "unlock", "update", "nvidia", "rewsl", 
        "getcho", "g1337x", "vsc", "autocomplete", 
        "cleanup", "get7z", "short2", "mas", 
        "getarm", "fixtime", "getdirectx", "getvc", 
        "rmgamebar", "getf4", "taskbar", "disadmin"
    ]
    
    # Run each function in sequence
    for function_name in ps_functions:
        status_text += f"\n=== RUNNING {function_name.upper()} ===\n"
        dpg.set_value("status_text", status_text)
        run_powershell_function(function_name)
        
        # Get updated status text after each function
        status_text = dpg.get_value("status_text")
        
    # Run Qaccess at the end
    status_text += "\n=== RUNNING QACCESS ===\n"
    dpg.set_value("status_text", status_text)
    qaccess_callback()
    
    # Final update
    status_text = dpg.get_value("status_text")
    status_text += "\n=== ALL AFTER FORMAT FUNCTIONS COMPLETED ===\n"
    dpg.set_value("status_text", status_text)

# Add specialized reboot functions
def run_bios_reboot():
    """Directly reboot to BIOS/UEFI firmware settings"""
    status_text = "Preparing to restart system into BIOS/UEFI firmware...\n"
    dpg.set_value("status_text", status_text)
    
    try:
        # Execute the shutdown command directly
        command = 'shutdown /r /fw /f /t 0'
        status_text += f"Executing: {command}\n"
        status_text += "Your computer will restart into BIOS/UEFI firmware settings immediately.\n"
        dpg.set_value("status_text", status_text)
        
        # Use a short delay to ensure the message is displayed before shutdown
        def delayed_shutdown():
            time.sleep(1)
            subprocess.run(command, shell=True)
            
        threading.Thread(target=delayed_shutdown, daemon=True).start()
    except Exception as e:
        status_text += f"Error: {str(e)}\n"
        dpg.set_value("status_text", status_text)

def run_rere_function():
    """Execute the rere PowerShell function that combines multiple functions"""
    status_text = "Running rere (update + network optimizations + reboot)...\n"
    dpg.set_value("status_text", status_text)
    
    ps_script = r'''
function rere {
    update; upnet; upnet2; upnet3; upnet4; reboot
}

# Execute the function
rere
'''
    
    try:
        # Create a temporary PS1 file
        with tempfile.NamedTemporaryFile(suffix='.ps1', delete=False) as temp_file:
            temp_file_path = temp_file.name
            temp_file.write(ps_script.encode('utf-8'))
        
        status_text += f"Created temporary script at: {temp_file_path}\n"
        
        # Execute PowerShell with elevated privileges if needed
        if is_admin():
            command = f'powershell.exe -ExecutionPolicy Bypass -File "{temp_file_path}"'
            status_text += f"Running rere as admin: {command}\n"
            status_text += "This will run updates, network optimizations, and then reboot your system.\n"
            dpg.set_value("status_text", status_text)
            
            # Run in separate thread
            def execute_rere():
                try:
                    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    # No need to wait for completion as this will reboot the system
                except Exception as e:
                    error_status = dpg.get_value("status_text")
                    error_status += f"Error executing rere: {str(e)}\n"
                    dpg.set_value("status_text", error_status)
                    
            threading.Thread(target=execute_rere, daemon=True).start()
        else:
            # Need to elevate
            status_text += "Requesting administrator privileges to run rere...\n"
            dpg.set_value("status_text", status_text)
            ctypes.windll.shell32.ShellExecuteW(None, "runas", "powershell.exe", f'-ExecutionPolicy Bypass -File "{temp_file_path}"', None, 1)
            status_text += "rere launched with admin rights in a new window.\n"
            dpg.set_value("status_text", status_text)
    except Exception as e:
        status_text += f"Error preparing rere: {str(e)}\n"
        status_text += traceback.format_exc() + "\n"
        dpg.set_value("status_text", status_text)

def run_safeboot_function():
    """Execute the SafeBoot PowerShell function"""
    status_text = "Running SafeBoot function...\n"
    dpg.set_value("status_text", status_text)
    
    ps_script = r'''
function SafeBoot {
    param (
        [Parameter(Mandatory=$false)]
        [ValidateSet("Minimal", "Network", "AlternateShell")]
        [string]$Mode = "Minimal",
        
        [Parameter(Mandatory=$false)]
        [switch]$Force,
        
        [Parameter(Mandatory=$false)]
        [int]$Timeout = 10
    )
    
    # Requires admin privileges
    if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
        Write-Error "ERROR: This function requires Administrator privileges. Please restart PowerShell as Administrator."
        return
    }
    
    try {
        # Verify bcdedit is available
        $bcdeditTest = bcdedit /enum | Out-String
        if (-not $?) {
            Write-Error "ERROR: Cannot access bcdedit. Make sure you're running as Administrator."
            return
        }
        
        # Configure boot settings with explicit output for debugging
        Write-Host "Configuring Safe Mode boot entry..." -ForegroundColor Cyan
        
        # Set up safe boot parameters
        switch ($Mode) {
            "Minimal" {
                $result = bcdedit /set '{current}' safeboot minimal
                Write-Host "bcdedit output: $result"
                Write-Host "Configured for Safe Mode (Minimal)" -ForegroundColor Green
            }
            "Network" {
                $result = bcdedit /set '{current}' safeboot network
                Write-Host "bcdedit output: $result"
                Write-Host "Configured for Safe Mode with Networking" -ForegroundColor Green
            }
            "AlternateShell" {
                $result1 = bcdedit /set '{current}' safeboot minimal
                $result2 = bcdedit /set '{current}' safebootalternateshell yes
                Write-Host "bcdedit output: $result1, $result2"
                Write-Host "Configured for Safe Mode with Command Prompt" -ForegroundColor Green
            }
        }
        
        # Verify the settings were applied
        Write-Host "Verifying boot configuration..." -ForegroundColor Cyan
        $verifyConfig = bcdedit /enum | Out-String
        
        if ($verifyConfig -match "safeboot\s+(\w+)") {
            Write-Host "Safe Boot configuration verified: $($Matches[1])" -ForegroundColor Green
            
            # Prompt for reboot
            if ($Force) {
                # Force restart without confirmation
                Write-Host "System will restart in $Timeout seconds..." -ForegroundColor Yellow
                Write-Host "WARNING: Your computer will boot into Safe Mode on the next restart." -ForegroundColor Red
                Start-Sleep -Seconds $Timeout
                shutdown.exe /r /t 0 /f
            } else {
                $confirm = Read-Host "System will restart into Safe Mode. Continue? (Y/N)"
                if ($confirm -eq "Y" -or $confirm -eq "y") {
                    Write-Host "Restarting system in 5 seconds..." -ForegroundColor Yellow
                    Write-Host "WARNING: Your computer will boot into Safe Mode on the next restart." -ForegroundColor Red
                    Start-Sleep -Seconds 5
                    shutdown.exe /r /t 0
                } else {
                    # Revert safe boot settings if user cancels
                    Write-Host "Reverting Safe Mode boot configuration..." -ForegroundColor Cyan
                    bcdedit /deletevalue '{current}' safeboot | Out-Null
                    bcdedit /deletevalue '{current}' safebootalternateshell 2>$null | Out-Null
                    Write-Host "Safe Mode boot configuration has been canceled and reverted." -ForegroundColor Yellow
                }
            }
        } else {
            Write-Error "ERROR: Failed to verify Safe Mode configuration. Safe Mode might not be properly configured."
            return
        }
    } catch {
        Write-Error "ERROR: An error occurred: $_"
        # Attempt to revert changes on error
        Write-Host "Attempting to revert boot configuration..." -ForegroundColor Yellow
        bcdedit /deletevalue '{current}' safeboot 2>$null | Out-Null
        bcdedit /deletevalue '{current}' safebootalternateshell 2>$null | Out-Null
    }
}

# Execute the function with default parameters
SafeBoot -Force -Timeout 5
'''
    
    try:
        # Create a temporary PS1 file
        with tempfile.NamedTemporaryFile(suffix='.ps1', delete=False) as temp_file:
            temp_file_path = temp_file.name
            temp_file.write(ps_script.encode('utf-8'))
        
        status_text += f"Created temporary script at: {temp_file_path}\n"
        
        # Execute PowerShell with elevated privileges (required for SafeBoot)
        if is_admin():
            command = f'powershell.exe -ExecutionPolicy Bypass -File "{temp_file_path}"'
            status_text += f"Running SafeBoot as admin: {command}\n"
            status_text += "WARNING: This will configure your system to boot into Safe Mode and restart.\n"
            dpg.set_value("status_text", status_text)
            
            def execute_safeboot():
                try:
                    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    # No need to wait as SafeBoot will restart
                except Exception as e:
                    error_status = dpg.get_value("status_text")
                    error_status += f"Error executing SafeBoot: {str(e)}\n"
                    dpg.set_value("status_text", error_status)
                    
            threading.Thread(target=execute_safeboot, daemon=True).start()
        else:
            # Need to elevate
            status_text += "Requesting administrator privileges to run SafeBoot...\n"
            dpg.set_value("status_text", status_text)
            ctypes.windll.shell32.ShellExecuteW(None, "runas", "powershell.exe", f'-ExecutionPolicy Bypass -File "{temp_file_path}"', None, 1)
            status_text += "SafeBoot launched with admin rights in a new window.\n"
            dpg.set_value("status_text", status_text)
    except Exception as e:
        status_text += f"Error preparing SafeBoot: {str(e)}\n"
        status_text += traceback.format_exc() + "\n"
        dpg.set_value("status_text", status_text)

def run_disable_safeboot_function():
    """Execute the DisableSafeBoot PowerShell function"""
    status_text = "Running DisableSafeBoot function...\n"
    dpg.set_value("status_text", status_text)
    
    ps_script = r'''
function DisableSafeBoot {
    # Requires admin privileges
    if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
        Write-Error "ERROR: This function requires Administrator privileges. Please restart PowerShell as Administrator."
        return
    }
    
    try {
        Write-Host "Removing Safe Mode boot configuration..." -ForegroundColor Cyan
        $result1 = bcdedit /deletevalue '{current}' safeboot
        $result2 = bcdedit /deletevalue '{current}' safebootalternateshell 2>$null
        
        Write-Host "Operation results: $result1, $result2"
        Write-Host "Safe Mode boot configuration has been removed. System will boot normally on next restart." -ForegroundColor Green
        
        $confirm = Read-Host "Do you want to restart the computer now? (Y/N)"
        if ($confirm -eq "Y" -or $confirm -eq "y") {
            Write-Host "Restarting system in 5 seconds..." -ForegroundColor Yellow
            Start-Sleep -Seconds 5
            shutdown.exe /r /t 0
        }
    } catch {
        Write-Error "ERROR: An error occurred: $_"
    }
}

# Execute the function
DisableSafeBoot
'''
    
    try:
        # Create a temporary PS1 file
        with tempfile.NamedTemporaryFile(suffix='.ps1', delete=False) as temp_file:
            temp_file_path = temp_file.name
            temp_file.write(ps_script.encode('utf-8'))
        
        status_text += f"Created temporary script at: {temp_file_path}\n"
        
        # Execute PowerShell with elevated privileges (required for DisableSafeBoot)
        if is_admin():
            command = f'powershell.exe -ExecutionPolicy Bypass -File "{temp_file_path}"'
            status_text += f"Running DisableSafeBoot as admin: {command}\n"
            dpg.set_value("status_text", status_text)
            
            def execute_disable_safeboot():
                try:
                    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    # Wait for user interaction in the PowerShell script
                except Exception as e:
                    error_status = dpg.get_value("status_text")
                    error_status += f"Error executing DisableSafeBoot: {str(e)}\n"
                    dpg.set_value("status_text", error_status)
                    
            threading.Thread(target=execute_disable_safeboot, daemon=True).start()
        else:
            # Need to elevate
            status_text += "Requesting administrator privileges to run DisableSafeBoot...\n"
            dpg.set_value("status_text", status_text)
            ctypes.windll.shell32.ShellExecuteW(None, "runas", "powershell.exe", f'-ExecutionPolicy Bypass -File "{temp_file_path}"', None, 1)
            status_text += "DisableSafeBoot launched with admin rights in a new window.\n"
            dpg.set_value("status_text", status_text)
    except Exception as e:
        status_text += f"Error preparing DisableSafeBoot: {str(e)}\n"
        status_text += traceback.format_exc() + "\n"
        dpg.set_value("status_text", status_text)

def create_gui():
    dpg.create_context()
    
    # Create a theme for the run button (green)
    with dpg.theme() as run_button_theme:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, [76, 209, 55])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [126, 255, 105])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [56, 179, 35])
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 5)
    
    # Create a theme for the close button (red)
    with dpg.theme() as close_button_theme:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, [209, 55, 55])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [255, 105, 105])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [179, 35, 35])
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 5)
    
    # Create a theme for the PS1 clean button (blue)
    with dpg.theme() as ps1_button_theme:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, [55, 120, 209])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [105, 170, 255])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [35, 100, 179])
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 5)
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 2)
    
    # Create a theme for the Qaccess button (purple)
    with dpg.theme() as qaccess_button_theme:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, [150, 55, 209])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [200, 105, 255])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [130, 35, 179])
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 5)
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 2)
    
    # Create a theme for the function buttons (orange)
    with dpg.theme() as function_button_theme:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, [209, 120, 55])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [255, 150, 105])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [179, 100, 35])
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 5, 3)
    
    # Create a theme for updates button (cyan)
    with dpg.theme() as updates_button_theme:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, [0, 150, 199])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [50, 200, 249])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [0, 120, 169])
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 5)

    # Create a theme for clear temps button (yellow)
    with dpg.theme() as clear_temps_button_theme:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, [199, 180, 0])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [249, 230, 50])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [169, 150, 0])
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 5)

    # Create a theme for run all button (gold)
    with dpg.theme() as run_all_button_theme:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, [212, 175, 55])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [255, 215, 0])
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [184, 134, 11])
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 5)
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 2)
    
    # Create a theme for the window
    with dpg.theme() as window_theme:
        with dpg.theme_component(dpg.mvWindowAppItem):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, [32, 32, 32])
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, [46, 46, 46])
    
    # Create a theme for tabs
    with dpg.theme() as tab_theme:
        with dpg.theme_component(dpg.mvTab):
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 5)
            dpg.add_theme_color(dpg.mvThemeCol_Tab, [40, 40, 40])
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered, [70, 70, 70])
            dpg.add_theme_color(dpg.mvThemeCol_TabActive, [60, 60, 80])
    
    # Configure viewport with new name
    dpg.create_viewport(title="Michael Fedro's Cleaning Suite", width=800, height=550)  # Increased height for tabs
    dpg.set_viewport_resize_callback(lambda s, d: dpg.set_item_width("main_window", d[0]-20))
    
    # Set up the main window with new name
    with dpg.window(tag="main_window", label="Michael Fedro's Cleaning Suite", width=800, height=550, no_resize=True, no_close=True):
        dpg.add_spacer(height=10)
        
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=15)
            with dpg.group():  # Removed width parameter here
                dpg.add_text("Welcome to Michael Fedro's Cleaning Suite", color=[255, 255, 255])
                dpg.add_text("Use the tabs below to access different tool categories", color=[200, 200, 200])
                dpg.add_spacer(height=20)
                
                # Add tab bar - removed width parameter
                with dpg.tab_bar(tag="main_tabs"):
                    # Cleanup tab
                    with dpg.tab(label="Cleanup", tag="tab_cleanup"):
                        dpg.add_spacer(height=15)
                        
                        # RUN ALL button at the top
                        with dpg.group(horizontal=True):
                            dpg.add_spacer(width=140)
                            run_all_button = dpg.add_button(
                                label="RUN ALL", 
                                callback=run_all_cleanup, 
                                width=300, 
                                height=70
                            )
                            dpg.bind_item_theme(run_all_button, run_all_button_theme)
                        
                        dpg.add_spacer(height=20)
                        
                        # First row of buttons
                        with dpg.group(horizontal=True):
                            dpg.add_spacer(width=25)
                            run_button = dpg.add_button(label="Run Tools", callback=run_tools_callback, width=200, height=60)
                            dpg.bind_item_theme(run_button, run_button_theme)
                            
                            dpg.add_spacer(width=20)
                            
                            close_button = dpg.add_button(label="Close Tools", callback=close_tools_callback, width=200, height=60)
                            dpg.bind_item_theme(close_button, close_button_theme)
                        
                        dpg.add_spacer(height=15)
                        
                        # Second row of buttons - PS1 clean and Updates
                        with dpg.group(horizontal=True):
                            dpg.add_spacer(width=25)
                            ps1_button = dpg.add_button(
                                label="PS1 CLEAN", 
                                callback=run_ps1_clean_callback, 
                                width=200, 
                                height=60
                            )
                            dpg.bind_item_theme(ps1_button, ps1_button_theme)
                            
                            dpg.add_spacer(width=20)
                            
                            updates_button = dpg.add_button(
                                label="Updates", 
                                callback=run_windows_updates, 
                                width=200, 
                                height=60
                            )
                            dpg.bind_item_theme(updates_button, updates_button_theme)
                        
                        dpg.add_spacer(height=15)
                        
                        # Third row - Force Delete button and Nvidia button
                        with dpg.group(horizontal=True):
                            dpg.add_spacer(width=25)
                            clear_temps_button = dpg.add_button(
                                label="FORCE DELETE ALL TEMP FILES", 
                                callback=clear_temp_files, 
                                width=200, 
                                height=60
                            )
                            dpg.bind_item_theme(clear_temps_button, clear_temps_button_theme)
                            
                            dpg.add_spacer(width=20)
                            
                            # Add Nvidia button to Cleanup tab
                            nvidia_button = dpg.add_button(
                                label="NVIDIA", 
                                callback=lambda s, a, u="nvidia": run_powershell_function(u),
                                width=200, 
                                height=60
                            )
                            dpg.bind_item_theme(nvidia_button, function_button_theme)
                    
                    # After Format tab
                    with dpg.tab(label="After Format", tag="tab_after_format"):
                        dpg.add_spacer(height=15)
                        
                        # Description
                        with dpg.group(horizontal=True):
                            dpg.add_spacer(width=25)
                            dpg.add_text("Tools to use after a fresh Windows installation", color=[220, 220, 220])
                        
                        dpg.add_spacer(height=20)
                        
                        # RUN ALL button at the top of After Format tab
                        with dpg.group(horizontal=True):
                            dpg.add_spacer(width=140)
                            after_format_run_all_button = dpg.add_button(
                                label="RUN ALL", 
                                callback=run_all_after_format, 
                                width=300, 
                                height=70
                            )
                            dpg.bind_item_theme(after_format_run_all_button, run_all_button_theme)
                        
                        dpg.add_spacer(height=20)
                        
                        # PowerShell function buttons in a grid layout
                        ps_functions = [
                            "unlock", "update", "nvidia", "rewsl", 
                            "getcho", "g1337x", "vsc", "autocomplete", 
                            "cleanup", "get7z", "short2", "mas", 
                            "getarm", "fixtime", "getdirectx", "getvc", 
                            "rmgamebar", "getf4", "taskbar", "disadmin"
                        ]
                        
                        # Group for all buttons - now with standard sizes
                        with dpg.group():
                            # Create grid layout with 2 buttons per row (because they're bigger now)
                            for i in range(0, len(ps_functions), 2):
                                with dpg.group(horizontal=True):
                                    dpg.add_spacer(width=25)
                                    for j in range(2):
                                        if i+j < len(ps_functions):
                                            function_name = ps_functions[i+j]
                                            button = dpg.add_button(
                                                label=function_name, 
                                                callback=lambda s, a, u: run_powershell_function(u),
                                                user_data=function_name,
                                                width=200,  # Standardized to 200
                                                height=60   # Standardized to 60
                                            )
                                            dpg.bind_item_theme(button, function_button_theme)
                                            dpg.add_spacer(width=20)
                                dpg.add_spacer(height=15)  # Increased spacing between rows
                        
                        dpg.add_spacer(height=15)
                        
                        # Qaccess button (already standard size at 200x60)
                        with dpg.group(horizontal=True):
                            dpg.add_spacer(width=140)
                            qaccess_button = dpg.add_button(
                                label="Qaccess", 
                                callback=qaccess_callback, 
                                width=200, 
                                height=60
                            )
                            dpg.bind_item_theme(qaccess_button, qaccess_button_theme)
                            
                    # Malware tab - new tab
                    with dpg.tab(label="Malware", tag="tab_malware"):
                        dpg.add_spacer(height=15)
                        
                        # Description
                        with dpg.group(horizontal=True):
                            dpg.add_spacer(width=25)
                            dpg.add_text("Tools for malware detection and removal", color=[220, 220, 220])
                        
                        dpg.add_spacer(height=20)
                        
                        # Malwarebytes button
                        with dpg.group(horizontal=True):
                            dpg.add_spacer(width=140)
                            malwarebytes_button = dpg.add_button(
                                label="Malwarebytes", 
                                callback=run_malwarebytes_install,
                                width=200, 
                                height=60
                            )
                            dpg.bind_item_theme(malwarebytes_button, function_button_theme)
                            
                        dpg.add_spacer(height=15)
                        
                        # RM malwarebytes button
                        with dpg.group(horizontal=True):
                            dpg.add_spacer(width=140)
                            rm_malwarebytes_button = dpg.add_button(
                                label="RM malwarebytes", 
                                callback=lambda: run_powershell_script(r"F:\study\shells\powershell\scripts\purgemalwarebytes.ps1"),
                                width=200, 
                                height=60
                            )
                            dpg.bind_item_theme(rm_malwarebytes_button, function_button_theme)
                        
                        dpg.add_spacer(height=15)
                        
                        # KVRT button
                        with dpg.group(horizontal=True):
                            dpg.add_spacer(width=140)
                            kvrt_button = dpg.add_button(
                                label="KVRT", 
                                callback=run_kvrt,
                                width=200, 
                                height=60
                            )
                            dpg.bind_item_theme(kvrt_button, function_button_theme)
                    
                    # Reboot tab - new tab
                    with dpg.tab(label="Reboot", tag="tab_reboot"):
                        dpg.add_spacer(height=15)
                        
                        # Description
                        with dpg.group(horizontal=True):
                            dpg.add_spacer(width=25)
                            dpg.add_text("Reboot options", color=[220, 220, 220])
                        
                        dpg.add_spacer(height=20)
                        
                        # Individual buttons with specific callbacks
                        with dpg.group():
                            # SafeBoot button
                            with dpg.group(horizontal=True):
                                dpg.add_spacer(width=140)
                                safeboot_button = dpg.add_button(
                                    label="safeboot",
                                    callback=run_safeboot_function,
                                    width=200,
                                    height=60
                                )
                                dpg.bind_item_theme(safeboot_button, function_button_theme)
                            dpg.add_spacer(height=15)
                            
                            # DisableSafeBoot button
                            with dpg.group(horizontal=True):
                                dpg.add_spacer(width=140)
                                disable_safeboot_button = dpg.add_button(
                                    label="DisableSafeBoot",
                                    callback=run_disable_safeboot_function,
                                    width=200,
                                    height=60
                                )
                                dpg.bind_item_theme(disable_safeboot_button, function_button_theme)
                            dpg.add_spacer(height=15)
                            
                            # rere button
                            with dpg.group(horizontal=True):
                                dpg.add_spacer(width=140)
                                rere_button = dpg.add_button(
                                    label="rere",
                                    callback=run_rere_function,
                                    width=200,
                                    height=60
                                )
                                dpg.bind_item_theme(rere_button, function_button_theme)
                            dpg.add_spacer(height=15)
                            
                            # bios button
                            with dpg.group(horizontal=True):
                                dpg.add_spacer(width=140)
                                bios_button = dpg.add_button(
                                    label="bios",
                                    callback=run_bios_reboot,
                                    width=200,
                                    height=60
                                )
                                dpg.bind_item_theme(bios_button, function_button_theme)
                            dpg.add_spacer(height=15)
                    
                    # Network tab - new tab
                    with dpg.tab(label="Network", tag="tab_network"):
                        dpg.add_spacer(height=15)
                        
                        # Description
                        with dpg.group(horizontal=True):
                            dpg.add_spacer(width=25)
                            dpg.add_text("Network-related tools", color=[220, 220, 220])
                        
                        dpg.add_spacer(height=20)
                        
                        # RUN ALL button at the top of Network tab
                        with dpg.group(horizontal=True):
                            dpg.add_spacer(width=140)
                            network_run_all_button = dpg.add_button(
                                label="RUN ALL", 
                                callback=lambda: threading.Thread(target=run_all_network_functions, daemon=True).start(),
                                width=300, 
                                height=70
                            )
                            dpg.bind_item_theme(network_run_all_button, run_all_button_theme)
                        
                        dpg.add_spacer(height=20)
                        
                        # Network function buttons in a grid layout
                        network_functions = ["upnet", "upnet2", "upnet3", "upnet4"]
                        
                        # Group for all buttons - now with standard sizes
                        with dpg.group():
                            # Create grid layout with 2 buttons per row
                            for i in range(0, len(network_functions), 2):
                                with dpg.group(horizontal=True):
                                    dpg.add_spacer(width=25)
                                    for j in range(2):
                                        if i+j < len(network_functions):
                                            function_name = network_functions[i+j]
                                            # Use special callback for upnet, standard callback for others
                                            if function_name == "upnet":
                                                button = dpg.add_button(
                                                    tag=f"network_button_{function_name}",
                                                    label=function_name,
                                                    callback=lambda s, a: run_upnet_function(), 
                                                    width=200,
                                                    height=60
                                                )
                                            elif function_name == "upnet2":
                                                button = dpg.add_button(
                                                    tag=f"network_button_{function_name}",
                                                    label=function_name,
                                                    callback=lambda s, a: run_upnet2_function(), 
                                                    width=200,
                                                    height=60
                                                )
                                            elif function_name == "upnet3":
                                                button = dpg.add_button(
                                                    tag=f"network_button_{function_name}",
                                                    label=function_name,
                                                    callback=lambda s, a: run_upnet3_function(), 
                                                    width=200,
                                                    height=60
                                                )
                                            elif function_name == "upnet4":
                                                button = dpg.add_button(
                                                    tag=f"network_button_{function_name}",
                                                    label=function_name,
                                                    callback=lambda s, a: run_upnet4_function(), 
                                                    width=200,
                                                    height=60
                                                )
                                            else:
                                                button = dpg.add_button(
                                                    tag=f"network_button_{function_name}",
                                                    label=function_name, 
                                                    callback=lambda s, a, u=function_name: run_powershell_function_threaded(u),
                                                    width=200,
                                                    height=60
                                                )
                                            dpg.bind_item_theme(button, function_button_theme)
                                dpg.add_spacer(height=15)

                dpg.bind_item_theme("main_tabs", tab_theme)
                
                dpg.add_spacer(height=20)
                dpg.add_separator()
                dpg.add_spacer(height=10)
                dpg.add_text("Status:", color=[255, 255, 255])
                dpg.add_text("Waiting for action...", tag="status_text", wrap=700, color=[200, 200, 200])
    
    # Apply the theme to the main window
    dpg.bind_item_theme("main_window", window_theme)
    
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("main_window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()

# Check if we need to run special commands as admin
if len(sys.argv) > 1:
    if sys.argv[1] == "--ps-clean-admin":
        try:
            # Read the path to the temp file from the flag file
            flag_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "run_ps_clean.flag")
            if os.path.exists(flag_file):
                with open(flag_file, 'r') as f:
                    temp_file_path = f.read().strip()
            
                if os.path.exists(temp_file_path):
                    # Execute PowerShell script with real-time output
                    print("Running PowerShell cleanup with real-time output...")
                    
                    # Create a process with piped output
                    process = subprocess.Popen(
                        f'powershell.exe -ExecutionPolicy Bypass -File "{temp_file_path}"',
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        bufsize=1,
                        universal_newlines=True
                    )
                    
                    # Read and display output in real-time
                    for line in iter(process.stdout.readline, ''):
                        print(line, end='')
                    
                    # Read any remaining output
                    stdout, stderr = process.communicate()
                    if stderr:
                        print(f"Errors: {stderr}")
                    
                    # Clean up
                    os.unlink(temp_file_path)
                
                # Remove flag file
                os.unlink(flag_file)
                
                print("PowerShell cleanup completed.")
            else:
                print("Flag file not found.")
                
        except Exception as e:
            print(f"Error running admin cleanup: {e}")
            print(traceback.format_exc())
        finally:
            input("Press Enter to exit...")
        sys.exit()
    elif sys.argv[1] == "--windows-updates":
        try:
            # Execute Windows Updates with real-time output
            print("Running Windows Updates with real-time output...")
            
            ps_command = '''
            if (-not (Get-Module -ListAvailable -Name PSWindowsUpdate)) { 
                Write-Host "Installing PSWindowsUpdate module..." -ForegroundColor Yellow
                Install-Module -Name PSWindowsUpdate -Force -AllowClobber -Scope CurrentUser 
            }; 
            Write-Host "Checking for and installing Windows Updates..." -ForegroundColor Cyan
            Get-WindowsUpdate -Install -AcceptAll -Verbose
            '''
            
            # Create a process with piped output
            process = subprocess.Popen(
                f'powershell.exe -ExecutionPolicy Bypass -Command "{ps_command}"',
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=1,
                universal_newlines=True
            )
            
            # Read and display output in real-time
            for line in iter(process.stdout.readline, ''):
                print(line, end='')
            
            # Read any remaining output
            stdout, stderr = process.communicate()
            if stderr:
                print(f"Errors: {stderr}")
                
            print("Windows Updates completed.")
        except Exception as e:
            print(f"Error running Windows Updates: {e}")
            print(traceback.format_exc())
        finally:
            input("Press Enter to exit...")
        sys.exit()
    elif sys.argv[1] == "--clear-temps":
        # Similar implementation for temp file cleanup with real-time output
        try:
            # Create temporary script file with real-time progress reporting
            temp_script = r'''
function Clear-AllTempFiles {
    Write-Host "Starting force deletion of ALL temp files..." -ForegroundColor Cyan
    
    # Common temp locations
    $locations = @(
        "$env:TEMP",
        "$env:WINDIR\Temp",
        "$env:WINDIR\Prefetch",
        "C:\Users\*\AppData\Local\Temp",
        "C:\Windows\SoftwareDistribution\Download",
        "C:\ProgramData\Microsoft\Windows\WER\ReportQueue",
        "C:\ProgramData\Microsoft\Windows\WER\ReportArchive",
        "C:\Users\*\AppData\Local\Microsoft\Windows\INetCache",
        "C:\Users\*\AppData\Local\Microsoft\Windows\WER",
        "C:\Users\*\AppData\Local\Microsoft\Terminal Server Client\Cache",
        "C:\Windows\Logs",
        "C:\Windows\Debug",
        "C:\Users\*\AppData\Local\CrashDumps",
        "C:\Users\*\AppData\Local\Microsoft\Windows\Explorer\ThumbCacheToDelete"
    )
    
    foreach ($location in $locations) {
        try {
            if (Test-Path -Path $location) {
                Write-Host "Force cleaning $location" -ForegroundColor Yellow
                # Count files first
                $fileCount = (Get-ChildItem -Path $location -Force -Recurse -ErrorAction SilentlyContinue | Where-Object { $_.PSIsContainer -eq $false }).Count
                Write-Host "$fileCount files found to clean..." -ForegroundColor Cyan
                
                # Delete files with progress
                $counter = 0
                $interval = [math]::Max(1, [math]::Floor($fileCount / 20)) # Report every 5% or at least every file
                
                Get-ChildItem -Path $location -Force -Recurse -ErrorAction SilentlyContinue | 
                Where-Object { $_.PSIsContainer -eq $false } | 
                ForEach-Object {
                    $counter++
                    try {
                        Remove-Item -Path $_.FullName -Force -ErrorAction SilentlyContinue
                        if ($counter % $interval -eq 0 -or $counter -eq $fileCount) {
                            Write-Progress -Activity "Cleaning $location" -Status "Removing files..." -PercentComplete (($counter / $fileCount) * 100)
                            Write-Host "Removed $counter of $fileCount files..." -ForegroundColor DarkGray
                        }
                    } catch {
                        # Continue silently
                    }
                }
                Write-Progress -Activity "Cleaning $location" -Completed
                Write-Host "Completed cleaning $location" -ForegroundColor Green
            }
        } catch {
            Write-Host "Failed to clean $location : $_" -ForegroundColor Red
        }
    }
    
    # Clear DNS cache
    ipconfig /flushdns
    Write-Host "DNS cache flushed" -ForegroundColor Green
    
    Write-Host "All temp files forcefully deleted!" -ForegroundColor Green
}

# Execute the function
Clear-AllTempFiles
'''
            # Write script to temporary file
            with tempfile.NamedTemporaryFile(suffix='.ps1', delete=False) as temp_file:
                temp_file_path = temp_file.name
                temp_file.write(temp_script.encode('utf-8'))
            
            print(f"Created temporary script at: {temp_file_path}")
            
            # Execute PowerShell script with real-time output
            command = f'powershell.exe -ExecutionPolicy Bypass -File "{temp_file_path}"'
            print(f"Running command: {command}")
            
            # Create a process with piped output
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=1,
                universal_newlines=True
            )
            
            # Read and display output in real-time
            for line in iter(process.stdout.readline, ''):
                print(line, end='')
            
            # Read any remaining output
            stdout, stderr = process.communicate()
            if stderr:
                print(f"Errors: {stderr}")
            
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
                print("Temporary script file cleaned up.")
            except:
                print("Could not delete temporary script file.")
                
            print("Temp file cleanup completed.")
        except Exception as e:
            print(f"Error clearing temp files: {e}")
            print(traceback.format_exc())
        finally:
            input("Press Enter to exit...")
        sys.exit()

def run_all_network_functions():
    """Run all network-related PowerShell functions in sequence"""
    status_text = "Running all network functions...\n"
    dpg.set_value("status_text", status_text)
    
    # List of all network-related PowerShell functions
    network_functions = ["upnet", "upnet2", "upnet3", "upnet4"]
    
    # Run each function in sequence
    for function_name in network_functions:
        status_text += f"\n=== RUNNING {function_name.upper()} ===\n"
        dpg.set_value("status_text", status_text)
        run_powershell_function(function_name)
        
        # Get updated status text after each function
        status_text = dpg.get_value("status_text")
    
    # Final update
    status_text += "\n=== ALL NETWORK FUNCTIONS COMPLETED ===\n"
    dpg.set_value("status_text", status_text)

def run_powershell_function_threaded(function_name):
    """Execute a PowerShell function in a separate thread to allow concurrent execution with real-time output"""
    threading.Thread(target=run_powershell_function, args=(function_name,), daemon=True).start()

def update_network_tab():
    """Update the Network tab to use direct function names and threaded execution"""
    # Define the network functions to display
    network_functions = ["upnet", "upnet2", "upnet3", "upnet4"]
    
    # For each function, update its callback to use threaded execution with the exact function name
    for i in range(0, len(network_functions), 2):
        for j in range(2):
            if i+j < len(network_functions):
                function_name = network_functions[i+j]
                # Create a unique identifier for each button
                button_tag = f"network_button_{function_name}"
                # Update the button's callback to use the threaded function
                if dpg.does_item_exist(button_tag):
                    dpg.set_item_callback(
                        button_tag, 
                        lambda s, a, u=function_name: run_powershell_function_threaded(u)
                    )

def run_upnet_function():
    """Execute the specific upnet PowerShell function with network optimizations and real-time output"""
    status_text = "Running upnet network optimization...\n"
    dpg.set_value("status_text", status_text)
    
    # Specific upnet PowerShell function with all network optimizations
    ps_script = r'''
function upnet {
    try {
        Write-Host "Starting network optimizations..." -ForegroundColor Cyan
        # Reset TCP/IP stack
        Write-Host "Resetting TCP/IP stack..." -ForegroundColor Yellow
        netsh int ip reset
        Write-Host "TCP/IP stack reset completed." -ForegroundColor Green

        # Release and renew IP address
        Write-Host "Releasing IP address..." -ForegroundColor Yellow
        ipconfig /release
        Write-Host "Renewing IP address..." -ForegroundColor Yellow
        ipconfig /renew
        Write-Host "IP address renewed." -ForegroundColor Green

        # Reset Winsock catalog
        Write-Host "Resetting Winsock catalog..." -ForegroundColor Yellow
        netsh winsock reset
        Write-Host "Winsock catalog reset completed." -ForegroundColor Green

        # Flush DNS cache
        Write-Host "Flushing DNS cache..." -ForegroundColor Yellow
        ipconfig /flushdns
        Clear-DnsClientCache
        Write-Host "DNS cache flushed." -ForegroundColor Green

        # Set TCP Global Parameters
        Write-Host "Setting TCP Global Parameters..." -ForegroundColor Yellow
        netsh int tcp set global autotuninglevel=normal
        netsh int tcp set global ecncapability=enabled
        netsh int tcp set global timestamps=disabled
        Write-Host "TCP Global Parameters set." -ForegroundColor Green

        # Retrieve Wi-Fi adapter name
        Write-Host "Finding Wi-Fi adapter..." -ForegroundColor Yellow
        $adapter = Get-NetAdapter | Where-Object {$_.Name -like "*Wi-Fi*"}
        if ($adapter) {
            Write-Host "Found Wi-Fi adapter: $($adapter.Name)" -ForegroundColor Green
            
            # Disable Large Send Offload (LSO)
            Write-Host "Disabling Large Send Offload (LSO)..." -ForegroundColor Yellow
            Disable-NetAdapterLso -Name $adapter.Name -ErrorAction SilentlyContinue
            Write-Host "LSO disabled." -ForegroundColor Green

            # Disable Receive Side Scaling (RSS)
            Write-Host "Disabling Receive Side Scaling (RSS)..." -ForegroundColor Yellow
            Set-NetAdapterRss -Name $adapter.Name -Enabled $false -ErrorAction SilentlyContinue
            Write-Host "RSS disabled." -ForegroundColor Green

            # Enable Packet Coalescing (only if available)
            Write-Host "Configuring Packet Coalescing..." -ForegroundColor Yellow
            Set-NetAdapterAdvancedProperty -Name $adapter.Name -DisplayName "Packet Coalescing" -DisplayValue "Enabled" -ErrorAction SilentlyContinue
            Write-Host "Packet Coalescing configured." -ForegroundColor Green

            # Disable Large Send Offload v2 (IPv4 & IPv6)
            Write-Host "Disabling Large Send Offload v2..." -ForegroundColor Yellow
            Set-NetAdapterAdvancedProperty -Name $adapter.Name -DisplayName "Large Send Offload v2 (IPv4)" -DisplayValue "Disabled" -ErrorAction SilentlyContinue
            Set-NetAdapterAdvancedProperty -Name $adapter.Name -DisplayName "Large Send Offload v2 (IPv6)" -DisplayValue "Disabled" -ErrorAction SilentlyContinue
            Write-Host "Large Send Offload v2 disabled." -ForegroundColor Green

            # Enable Jumbo Frames (if supported)
            Write-Host "Configuring Jumbo Frames..." -ForegroundColor Yellow
            Set-NetAdapterAdvancedProperty -Name $adapter.Name -DisplayName "Jumbo Packet" -DisplayValue "9014" -ErrorAction SilentlyContinue
            Write-Host "Jumbo Frames configured." -ForegroundColor Green

            # Disable Network Throttling Index
            Write-Host "Disabling Network Throttling Index..." -ForegroundColor Yellow
            Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" -Name "NetworkThrottlingIndex" -Value 0xffffffff -ErrorAction SilentlyContinue
            Write-Host "Network Throttling Index disabled." -ForegroundColor Green

            # Disable TCP Task Offload
            Write-Host "Disabling TCP Task Offload..." -ForegroundColor Yellow
            Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" -Name "DisableTaskOffload" -Value 1 -ErrorAction SilentlyContinue
            Write-Host "TCP Task Offload disabled." -ForegroundColor Green

            # Restart Wi-Fi adapter
            Write-Host "Restarting Wi-Fi adapter..." -ForegroundColor Yellow
            Restart-NetAdapter -Name $adapter.Name
            Write-Host "Wi-Fi adapter restarted." -ForegroundColor Green
        } else {
            Write-Host "Wi-Fi adapter not found. Skipping adapter-specific settings." -ForegroundColor Red
        }

        # DNS Settings
        Write-Host "Setting DNS to Google DNS servers..." -ForegroundColor Yellow
        Set-DnsClientServerAddress -InterfaceAlias "Wi-Fi" -ServerAddresses ("8.8.8.8", "8.8.4.4")
        Write-Host "DNS set to Google servers." -ForegroundColor Green

        # Set High Performance Power Plan
        Write-Host "Setting High Performance power plan..." -ForegroundColor Yellow
        powercfg -setactive SCHEME_MIN
        Write-Host "Power plan set to High Performance." -ForegroundColor Green

        # Set Default Gateway Metric for faster routing
        Write-Host "Optimizing default gateway metric..." -ForegroundColor Yellow
        $gateway = (Get-NetIPConfiguration | Where-Object {$_.InterfaceAlias -like "Wi-Fi"}).IPv4DefaultGateway
        if ($gateway) {
            Set-NetRoute -DestinationPrefix "0.0.0.0/0" -NextHop $gateway.NextHop -RouteMetric 1
            Write-Host "Default gateway metric optimized." -ForegroundColor Green
        }

        Write-Host "Network optimizations applied successfully. You may need to restart your computer for all changes to take effect." -ForegroundColor Cyan
    } catch {
        Write-Host "An error occurred: $_" -ForegroundColor Red
    }
}

# Execute the function
upnet
'''
    
    try:
        # Create a temporary PS1 file
        with tempfile.NamedTemporaryFile(suffix='.ps1', delete=False) as temp_file:
            temp_file_path = temp_file.name
            temp_file.write(ps_script.encode('utf-8'))
        
        status_text += f"Created temporary script for upnet at: {temp_file_path}\n"
        
        # Execute PowerShell with elevated privileges if needed
        if is_admin():
            # Already admin, run directly
            command = f'powershell.exe -ExecutionPolicy Bypass -File "{temp_file_path}"'
            status_text += f"Running upnet as admin: {command}\n"
            dpg.set_value("status_text", status_text)
            
            # Use the real-time output function
            status_text, returncode = run_powershell_with_realtime_output(command, status_text, temp_file_path)
        else:
            # Need to elevate - this part is simplified since upnet needs admin rights
            status_text += "Requesting administrator privileges to run upnet network optimizations...\n"
            dpg.set_value("status_text", status_text)
            ctypes.windll.shell32.ShellExecuteW(None, "runas", "powershell.exe", f'-ExecutionPolicy Bypass -File "{temp_file_path}"', None, 1)
            status_text += "upnet launched with admin rights in a new window.\n"
            dpg.set_value("status_text", status_text)
    except Exception as e:
        status_text += f"Error preparing upnet: {str(e)}\n"
        status_text += traceback.format_exc() + "\n"
        dpg.set_value("status_text", status_text)

def run_upnet2_function():
    """Execute the specific upnet2 PowerShell function with advanced network optimizations"""
    status_text = "Running upnet2 advanced network optimization...\n"
    dpg.set_value("status_text", status_text)
    
    # Specific upnet2 PowerShell function with comprehensive network optimizations
    ps_script = r'''
function upnet2 {
    [CmdletBinding()]
    param()

    try {
        Write-Host "Starting network optimization process..." -ForegroundColor Cyan

        # Ensure the script is running with administrative privileges
        if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
            Write-Error "You must run this script as an administrator."
            return
        }

        # Reset TCP/IP stack
        Write-Host "Resetting TCP/IP stack..." -ForegroundColor Green
        netsh int ip reset
        Write-Host "TCP/IP stack reset successfully." -ForegroundColor Yellow

        # Release and renew IP address
        Write-Host "Releasing IP address..." -ForegroundColor Green
        ipconfig /release
        Write-Host "IP address released." -ForegroundColor Yellow

        Write-Host "Renewing IP address..." -ForegroundColor Green
        ipconfig /renew
        Write-Host "IP address renewed." -ForegroundColor Yellow

        # Flush DNS cache
        Write-Host "Flushing DNS cache..." -ForegroundColor Green
        ipconfig /flushdns
        Write-Host "DNS cache flushed." -ForegroundColor Yellow

        # Reset Winsock catalog
        Write-Host "Resetting Winsock catalog..." -ForegroundColor Green
        netsh winsock reset
        Write-Host "Winsock catalog reset successfully." -ForegroundColor Yellow

        # Clear ARP cache
        Write-Host "Clearing ARP cache..." -ForegroundColor Green
        netsh interface ip delete arpcache
        Write-Host "ARP cache cleared." -ForegroundColor Yellow

        # Reset routing table
        Write-Host "Resetting routing table..." -ForegroundColor Green
        route -f
        Write-Host "Routing table reset." -ForegroundColor Yellow

        # Adjust TCP settings
        Write-Host "Configuring TCP settings..." -ForegroundColor Green

        # Disable Auto-Tuning
        netsh interface tcp set global autotuninglevel=disabled
        Write-Host "Windows Auto-Tuning disabled." -ForegroundColor Yellow

        # Disable Scaling Heuristics
        netsh interface tcp set heuristics=disabled
        Write-Host "Windows Scaling Heuristics disabled." -ForegroundColor Yellow

        # Set Congestion Provider to CTCP (Correct Command)
        netsh int tcp set supplemental congestionprovider=ctcp
        Write-Host "Congestion Provider set to CTCP." -ForegroundColor Yellow

        # Enable ECN Capability
        netsh int tcp set global ecncapability=enabled
        Write-Host "ECN Capability enabled." -ForegroundColor Yellow

        # Set MTU size to 1500 for active adapters
        Write-Host "Setting MTU size to 1500 for active adapters..." -ForegroundColor Green
        $activeAdapters = Get-NetAdapter | Where-Object { $_.Status -eq "Up" -and $_.NdisPhysicalMedium -ne "Native802_11" }
        foreach ($adapter in $activeAdapters) {
            try {
                Set-NetAdapterAdvancedProperty -Name $adapter.Name -DisplayName "MTU" -DisplayValue "1500" -ErrorAction Stop
                Write-Host "MTU set to 1500 on adapter: $($adapter.Name)" -ForegroundColor Yellow
            } catch {
                Write-Warning "Failed to set MTU on adapter: $($adapter.Name). It may not support this property."
            }
        }

        # Restart network adapters
        Write-Host "Restarting network adapters..." -ForegroundColor Green
        foreach ($adapter in $activeAdapters) {
            try {
                Disable-NetAdapter -Name $adapter.Name -Confirm:$false -ErrorAction Stop
                Start-Sleep -Seconds 2
                Enable-NetAdapter -Name $adapter.Name -Confirm:$false -ErrorAction Stop
                Write-Host "Restarted adapter: $($adapter.Name)" -ForegroundColor Yellow
            } catch {
                Write-Warning "Failed to restart adapter: $($adapter.Name)."
            }
        }

        # Remove proxy settings
        Write-Host "Removing proxy settings..." -ForegroundColor Green
        netsh winhttp reset proxy
        Write-Host "Proxy settings removed." -ForegroundColor Yellow

        # Disable Large Send Offload where applicable
        Write-Host "Disabling Large Send Offload on applicable adapters..." -ForegroundColor Green
        foreach ($adapter in $activeAdapters) {
            $properties = Get-NetAdapterAdvancedProperty -Name $adapter.Name -ErrorAction SilentlyContinue
            if ($properties) {
                foreach ($property in $properties) {
                    if ($property.DisplayName -like "*Large Send Offload*") {
                        try {
                            Set-NetAdapterAdvancedProperty -Name $adapter.Name -DisplayName $property.DisplayName -DisplayValue "Disabled" -ErrorAction Stop
                            Write-Host "Disabled $($property.DisplayName) on adapter: $($adapter.Name)" -ForegroundColor Yellow
                        } catch {
                            Write-Warning "Failed to disable $($property.DisplayName) on adapter: $($adapter.Name)."
                        }
                    }
                }
            }
        }

        # Restart essential network services
        Write-Host "Restarting essential network services..." -ForegroundColor Green
        $servicesToRestart = @("Dhcp", "Dnscache", "NlaSvc", "netprofm", "WlanSvc", "dot3svc")
        foreach ($service in $servicesToRestart) {
            try {
                if (Get-Service -Name $service -ErrorAction SilentlyContinue) {
                    Restart-Service -Name $service -Force -ErrorAction Stop
                    Write-Host "Service '$service' restarted successfully." -ForegroundColor Yellow
                } else {
                    Write-Warning "Service '$service' does not exist."
                }
            } catch {
                Write-Warning "Failed to restart service '$service'. It might be dependent on other services or require a reboot."
            }
        }

        # Remove lingering network connections
        Write-Host "Removing lingering network connections..." -ForegroundColor Green
        net use * /delete /yes 2>$null
        Write-Host "Lingering network connections removed." -ForegroundColor Yellow

        # Update Group Policy settings
        Write-Host "Updating Group Policy settings..." -ForegroundColor Green
        gpupdate /force
        Write-Host "Group Policy settings updated." -ForegroundColor Yellow

        # Re-register DNS
        Write-Host "Re-registering DNS..." -ForegroundColor Green
        ipconfig /registerdns
        Write-Host "DNS re-registration initiated." -ForegroundColor Yellow

        # Synchronize time settings
        Write-Host "Synchronizing time settings..." -ForegroundColor Green
        try {
            w32tm /resync
            Write-Host "Time synchronization successful." -ForegroundColor Yellow
        } catch {
            Write-Warning "Time synchronization failed. Ensure the Windows Time service is running."
        }

        # Set DNS servers to Google DNS for active adapters
        Write-Host "Setting DNS servers to Google DNS for active adapters..." -ForegroundColor Green
        foreach ($adapter in $activeAdapters) {
            try {
                Set-DnsClientServerAddress -InterfaceAlias $adapter.Name -ServerAddresses ("8.8.8.8","8.8.4.4") -ErrorAction Stop
                Write-Host "DNS servers set to Google DNS on adapter: $($adapter.Name)" -ForegroundColor Yellow
            } catch {
                Write-Warning "Failed to set DNS servers on adapter: $($adapter.Name)."
            }
        }

        # Reset advanced firewall settings
        Write-Host "Resetting advanced firewall settings..." -ForegroundColor Green
        netsh advfirewall reset
        Write-Host "Advanced firewall settings reset." -ForegroundColor Yellow

        # Enable QoS Packet Scheduler where applicable
        Write-Host "Enabling QoS Packet Scheduler on applicable adapters..." -ForegroundColor Green
        foreach ($adapter in $activeAdapters) {
            try {
                # Check if QoS Packet Scheduler is available
                $qosProperty = Get-NetAdapterAdvancedProperty -Name $adapter.Name -DisplayName "QoS Packet Scheduler" -ErrorAction SilentlyContinue
                if ($qosProperty) {
                    Set-NetAdapterAdvancedProperty -Name $adapter.Name -DisplayName "QoS Packet Scheduler" -DisplayValue "Enabled" -ErrorAction Stop
                    Write-Host "QoS Packet Scheduler enabled on adapter: $($adapter.Name)" -ForegroundColor Yellow
                } else {
                    Write-Warning "QoS Packet Scheduler not found on adapter: $($adapter.Name)."
                }
            } catch {
                Write-Warning "Failed to enable QoS Packet Scheduler on adapter: $($adapter.Name)."
            }
        }

        # Optimize network adapter power management settings
        Write-Host "Optimizing network adapter power management settings..." -ForegroundColor Green
        foreach ($adapter in $activeAdapters) {
            try {
                Set-NetAdapterPowerManagement -Name $adapter.Name -NoPowerSaving -ErrorAction Stop
                Write-Host "Power management optimized on adapter: $($adapter.Name)" -ForegroundColor Yellow
            } catch {
                Write-Warning "Failed to optimize power management on adapter: $($adapter.Name)."
            }
        }

        # Optimize network adapter advanced settings
        Write-Host "Optimizing network adapter advanced settings..." -ForegroundColor Green
        foreach ($adapter in $activeAdapters) {
            $properties = Get-NetAdapterAdvancedProperty -Name $adapter.Name -ErrorAction SilentlyContinue
            if ($properties) {
                foreach ($property in $properties) {
                    switch ($property.DisplayName) {
                        "Receive Side Scaling" {
                            try {
                                Set-NetAdapterAdvancedProperty -Name $adapter.Name -DisplayName "Receive Side Scaling" -DisplayValue "Enabled" -ErrorAction Stop
                                Write-Host "Receive Side Scaling enabled on adapter: $($adapter.Name)" -ForegroundColor Yellow
                            } catch {
                                Write-Warning "Failed to enable Receive Side Scaling on adapter: $($adapter.Name)."
                            }
                        }
                        "Interrupt Moderation" {
                            try {
                                Set-NetAdapterAdvancedProperty -Name $adapter.Name -DisplayName "Interrupt Moderation" -DisplayValue "Enabled" -ErrorAction Stop
                                Write-Host "Interrupt Moderation enabled on adapter: $($adapter.Name)" -ForegroundColor Yellow
                            } catch {
                                Write-Warning "Failed to enable Interrupt Moderation on adapter: $($adapter.Name)."
                            }
                        }
                        default {}
                    }
                }
            }
        }

        # Display network statistics
        Write-Host "Displaying network statistics..." -ForegroundColor Green
        netstat -e
        Write-Host "Network statistics displayed." -ForegroundColor Yellow

        Write-Host "Network optimization complete. A system reboot is recommended to apply all changes." -ForegroundColor Cyan

    } catch {
        Write-Error "An unexpected error occurred: $_"
    }
}

# Execute the function
upnet2
'''
    
    try:
        # Create a temporary PS1 file
        with tempfile.NamedTemporaryFile(suffix='.ps1', delete=False) as temp_file:
            temp_file_path = temp_file.name
            temp_file.write(ps_script.encode('utf-8'))
        
        status_text += f"Created temporary script for upnet2 at: {temp_file_path}\n"
        
        # Execute PowerShell with elevated privileges if needed
        if is_admin():
            # Already admin, run directly
            command = f'powershell.exe -ExecutionPolicy Bypass -File "{temp_file_path}"'
            status_text += f"Running upnet2 as admin: {command}\n"
            dpg.set_value("status_text", status_text)
            
            # Use the real-time output function
            status_text, returncode = run_powershell_with_realtime_output(command, status_text, temp_file_path)
        else:
            # Need to elevate - this part is simplified since upnet2 needs admin rights
            status_text += "Requesting administrator privileges to run upnet2 network optimizations...\n"
            dpg.set_value("status_text", status_text)
            ctypes.windll.shell32.ShellExecuteW(None, "runas", "powershell.exe", f'-ExecutionPolicy Bypass -File "{temp_file_path}"', None, 1)
            status_text += "upnet2 launched with admin rights in a new window.\n"
            dpg.set_value("status_text", status_text)
    except Exception as e:
        status_text += f"Error preparing upnet2: {str(e)}\n"
        status_text += traceback.format_exc() + "\n"
        dpg.set_value("status_text", status_text)

def run_upnet3_function():
    """Execute the comprehensive WiFi optimization PowerShell function (upnet3)"""
    status_text = "Running upnet3 comprehensive WiFi optimization...\n"
    dpg.set_value("status_text", status_text)
    
    # Comprehensive WiFi optimization PowerShell script
    ps_script = r'''
function upnet3 {
    [CmdletBinding()]
    param()

    try {
        Write-Host "Starting comprehensive WiFi optimization..." -ForegroundColor Cyan

        # Admin check
        if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
            throw "Please run as administrator!"
        }

        # Advanced WiFi optimizations
        netsh wlan set autoconfig enabled=yes interface="Wi-Fi"
        netsh int tcp set supplemental Internet congestionprovider=ctcp
        netsh int tcp set heuristics disabled
        netsh int tcp set global initialRto=2000
        netsh int tcp set global timestamps=disabled
        netsh int tcp set global nonsackrttresiliency=disabled
        netsh int tcp set global rsc=enabled
        netsh int tcp set global ecncapability=disabled
        netsh int tcp set global dca=enabled
        netsh int tcp set global netdma=enabled
        netsh int tcp set global timestamps=disabled

        # Power management optimizations
        powershell -Command "Get-NetAdapter -Name 'Wi-Fi' | Set-NetAdapterPowerManagement -SelectiveSuspend Disabled"
        powercfg -change -monitor-timeout-ac 0
        powercfg -change -monitor-timeout-dc 0
        powercfg /setacvalueindex scheme_current sub_processor PROCTHROTTLEMAX 100
        powercfg /setdcvalueindex scheme_current sub_processor PROCTHROTTLEMAX 100

        # Advanced network settings
        Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" -Name "DefaultTTL" -Value 64
        Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" -Name "TCPNoDelay" -Value 1
        Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" -Name "Tcp1323Opts" -Value 1
        Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile" -Name "NetworkThrottlingIndex" -Value 0xffffffff
        Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile" -Name "SystemResponsiveness" -Value 0

        # QoS and bandwidth optimization
        netsh int tcp set global autotuninglevel=normal
        netsh int tcp set global chimney=enabled
        netsh int ip set global taskoffload=enabled
        netsh int ip set global neighborcachelimit=4096
        netsh int tcp set global windowsscaling=enabled

        # WiFi-specific optimizations
        netsh wlan set autoconfig enabled=yes interface="Wi-Fi"
        netsh wlan set allowexplicitcreds allow=yes
        netsh wlan set hostednetwork mode=allow
        
        # Clear DNS and network caches
        ipconfig /flushdns
        ipconfig /registerdns
        nbtstat -R
        nbtstat -RR
        arp -d *
        route -f

        # Set optimal MTU
        $adapter = Get-NetAdapter | Where-Object {$_.Name -eq "Wi-Fi"}
        Set-NetIPInterface -InterfaceIndex $adapter.ifIndex -NlMtuBytes 1500

        # Disable IPv6 temporary addresses
        Set-NetIPv6Protocol -RandomizeIdentifiers Disabled
        
        # Optimize receive window auto-tuning
        netsh int tcp set global autotuninglevel=normal
        
        # Reset network stack thoroughly
        netsh int ip reset C:\resetlog.txt
        netsh int ipv6 reset C:\resetlogv6.txt
        
        # Optimize network bindings
        Get-NetAdapter | Set-NetAdapterBinding -ComponentID 'ms_tcpip6' -Enabled $false
        Get-NetAdapter | Set-NetAdapterBinding -ComponentID 'ms_msclient' -Enabled $false
        
        # Set network adapter properties
        Set-NetAdapterAdvancedProperty -Name "Wi-Fi" -DisplayName "Packet Coalescing" -DisplayValue "Disabled" -ErrorAction SilentlyContinue
        Set-NetAdapterAdvancedProperty -Name "Wi-Fi" -DisplayName "Power Saving Mode" -DisplayValue "Disabled" -ErrorAction SilentlyContinue

        Write-Host "All WiFi optimizations completed! Please restart your computer." -ForegroundColor Green
    }
    catch {
        Write-Error "An error occurred: $_"
    }
}

# Execute the function
upnet3
'''
    
    try:
        # Create a temporary PS1 file
        with tempfile.NamedTemporaryFile(suffix='.ps1', delete=False) as temp_file:
            temp_file_path = temp_file.name
            temp_file.write(ps_script.encode('utf-8'))
        
        status_text += f"Created temporary script for upnet3 at: {temp_file_path}\n"
        
        # Execute PowerShell with elevated privileges if needed
        if is_admin():
            # Already admin, run directly
            command = f'powershell.exe -ExecutionPolicy Bypass -File "{temp_file_path}"'
            status_text += f"Running upnet3 as admin: {command}\n"
            dpg.set_value("status_text", status_text)
            
            # Use the real-time output function
            status_text, returncode = run_powershell_with_realtime_output(command, status_text, temp_file_path)
        else:
            # Need to elevate
            status_text += "Requesting administrator privileges to run upnet3 WiFi optimizations...\n"
            dpg.set_value("status_text", status_text)
            ctypes.windll.shell32.ShellExecuteW(None, "runas", "powershell.exe", f'-ExecutionPolicy Bypass -File "{temp_file_path}"', None, 1)
            status_text += "upnet3 launched with admin rights in a new window.\n"
            dpg.set_value("status_text", status_text)
    except Exception as e:
        status_text += f"Error preparing upnet3: {str(e)}\n"
        status_text += traceback.format_exc() + "\n"
        dpg.set_value("status_text", status_text)

def run_upnet4_function():
    """Execute the ultra comprehensive WiFi optimization PowerShell function (upnet4)"""
    status_text = "Running upnet4 ultra comprehensive WiFi optimization...\n"
    dpg.set_value("status_text", status_text)
    
    # Ultra comprehensive WiFi optimization PowerShell script
    ps_script = r'''
function upnet4 {
    [CmdletBinding()]
    param()

    try {
        Write-Host "Starting ultra comprehensive WiFi optimization (upnet4)..." -ForegroundColor Cyan

        # Check for administrative privileges
        if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
            throw "Please run this script as an administrator!"
        }

        # Dynamically find the Wi-Fi adapter by matching common names or descriptions.
        $wifiAdapter = Get-NetAdapter | Where-Object { 
            $_.InterfaceDescription -match "Wireless" -or 
            $_.Name -match "Wi[- ]?Fi" 
        } | Select-Object -First 1

        # Fallback search if not found above
        if (-not $wifiAdapter) {
            Write-Host "Wi-Fi adapter not found by name. Trying fallback search using '802.11'..." -ForegroundColor Yellow
            $wifiAdapter = Get-NetAdapter | Where-Object { $_.InterfaceDescription -match "802.11" } | Select-Object -First 1
        }

        if (-not $wifiAdapter) {
            Write-Error "Wi-Fi adapter not found. Exiting function."
            return
        }

        Write-Host "Using Wi-Fi adapter: $($wifiAdapter.Name)" -ForegroundColor Green

        # 1. Disable Large Send Offload (IPv4 and IPv6)
        Write-Host "Disabling Large Send Offload (IPv4 and IPv6)..." -ForegroundColor Yellow
        Set-NetAdapterAdvancedProperty -Name $wifiAdapter.Name -DisplayName "Large Send Offload V2 (IPv4)" -DisplayValue "Disabled" -ErrorAction SilentlyContinue
        Set-NetAdapterAdvancedProperty -Name $wifiAdapter.Name -DisplayName "Large Send Offload V2 (IPv6)" -DisplayValue "Disabled" -ErrorAction SilentlyContinue

        # 2. Set Roaming Aggressiveness to Highest
        Write-Host "Setting Roaming Aggressiveness to Highest..." -ForegroundColor Yellow
        Set-NetAdapterAdvancedProperty -Name $wifiAdapter.Name -DisplayName "Roaming Aggressiveness" -DisplayValue "Highest" -ErrorAction SilentlyContinue

        # 3. Configure TCP ACK settings
        Write-Host "Configuring TCP ACK settings..." -ForegroundColor Yellow
        New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" -Name "TCPAckFrequency" -PropertyType DWord -Value 1 -Force | Out-Null

        # 4. Enable TCP Fast Open (if supported)
        Write-Host "Enabling TCP Fast Open (if supported)..." -ForegroundColor Yellow
        netsh int tcp set global fastopen=enabled 2>$null

        # 5. Disable Interrupt Moderation
        Write-Host "Disabling Interrupt Moderation..." -ForegroundColor Yellow
        Set-NetAdapterAdvancedProperty -Name $wifiAdapter.Name -DisplayName "Interrupt Moderation" -DisplayValue "Disabled" -ErrorAction SilentlyContinue

        # 6. Disable Energy Efficient Ethernet (EEE)
        Write-Host "Disabling Energy Efficient Ethernet (EEE)..." -ForegroundColor Yellow
        Set-NetAdapterAdvancedProperty -Name $wifiAdapter.Name -DisplayName "Energy Efficient Ethernet" -DisplayValue "Disabled" -ErrorAction SilentlyContinue

        # 7. Disable Task Offload via registry tweak
        Write-Host "Applying registry tweak: Disable Task Offload..." -ForegroundColor Yellow
        New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" -Name "DisableTaskOffload" -PropertyType DWord -Value 1 -Force | Out-Null

        # 8. Disable Receive Side Scaling (RSS)
        Write-Host "Disabling Receive Side Scaling (RSS)..." -ForegroundColor Yellow
        Set-NetAdapterAdvancedProperty -Name $wifiAdapter.Name -DisplayName "Receive Side Scaling" -DisplayValue "Disabled" -ErrorAction SilentlyContinue

        # 9. Disable TCP and UDP Checksum Offload
        Write-Host "Disabling TCP and UDP Checksum Offload..." -ForegroundColor Yellow
        Set-NetAdapterAdvancedProperty -Name $wifiAdapter.Name -DisplayName "TCP Checksum Offload" -DisplayValue "Disabled" -ErrorAction SilentlyContinue
        Set-NetAdapterAdvancedProperty -Name $wifiAdapter.Name -DisplayName "UDP Checksum Offload" -DisplayValue "Disabled" -ErrorAction SilentlyContinue

        # 10. Disable Power Saving Mode on the adapter (if parameter available)
        Write-Host "Disabling Power Saving Mode on the adapter..." -ForegroundColor Yellow
        try {
            Set-NetAdapterPowerManagement -Name $wifiAdapter.Name -AllowComputerToTurnOffDevice $false -ErrorAction Stop
        }
        catch {
            Write-Host "Skipping Set-NetAdapterPowerManagement tweak: parameter not available." -ForegroundColor Yellow
        }

        # 11. Set Transmit Power to Highest
        Write-Host "Setting Transmit Power to Highest..." -ForegroundColor Yellow
        Set-NetAdapterAdvancedProperty -Name $wifiAdapter.Name -DisplayName "Transmit Power" -DisplayValue "Highest" -ErrorAction SilentlyContinue

        # 12. Force wireless mode to 802.11n (if supported)
        Write-Host "Forcing wireless mode to 802.11n (if supported)..." -ForegroundColor Yellow
        Set-NetAdapterAdvancedProperty -Name $wifiAdapter.Name -DisplayName "Wireless Mode" -DisplayValue "802.11n" -ErrorAction SilentlyContinue

        # 13. Additional tweak: Disable 802.11 Power Save
        Write-Host "Disabling 802.11 Power Save..." -ForegroundColor Yellow
        netsh wlan set profileparameter name=$wifiAdapter.Name powerManagement=disabled 2>$null

        # 14. Additional tweak: Set Preferred Band to 5GHz (if supported)
        Write-Host "Setting Preferred Band to 5GHz (if supported)..." -ForegroundColor Yellow
        Set-NetAdapterAdvancedProperty -Name $wifiAdapter.Name -DisplayName "Preferred Band" -DisplayValue "5 GHz" -ErrorAction SilentlyContinue

        # Restart the Wi-Fi adapter to apply changes
        Write-Host "Restarting the Wi-Fi adapter to apply changes..." -ForegroundColor Yellow
        Disable-NetAdapter -Name $wifiAdapter.Name -Confirm:$false -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 2
        Enable-NetAdapter -Name $wifiAdapter.Name -Confirm:$false -ErrorAction SilentlyContinue

        Write-Host "Displaying current Wi-Fi adapter status:" -ForegroundColor Cyan
        netsh wlan show interfaces

        Write-Host "Ultra comprehensive WiFi optimization (upnet4) completed! A system restart is recommended." -ForegroundColor Green
    }
    catch {
        Write-Error "An error occurred in upnet4: $_"
    }
}

# Execute the function
upnet4
'''
    
    try:
        # Create a temporary PS1 file
        with tempfile.NamedTemporaryFile(suffix='.ps1', delete=False) as temp_file:
            temp_file_path = temp_file.name
            temp_file.write(ps_script.encode('utf-8'))
        
        status_text += f"Created temporary script for upnet4 at: {temp_file_path}\n"
        
        # Execute PowerShell with elevated privileges if needed
        if is_admin():
            # Already admin, run directly
            command = f'powershell.exe -ExecutionPolicy Bypass -File "{temp_file_path}"'
            status_text += f"Running upnet4 as admin: {command}\n"
            dpg.set_value("status_text", status_text)
            
            # Use the real-time output function
            status_text, returncode = run_powershell_with_realtime_output(command, status_text, temp_file_path)
        else:
            # Need to elevate
            status_text += "Requesting administrator privileges to run upnet4 WiFi optimizations...\n"
            dpg.set_value("status_text", status_text)
            ctypes.windll.shell32.ShellExecuteW(None, "runas", "powershell.exe", f'-ExecutionPolicy Bypass -File "{temp_file_path}"', None, 1)
            status_text += "upnet4 launched with admin rights in a new window.\n"
            dpg.set_value("status_text", status_text)
    except Exception as e:
        status_text += f"Error preparing upnet4: {str(e)}\n"
        status_text += traceback.format_exc() + "\n"
        dpg.set_value("status_text", status_text)

if __name__ == "__main__":
    # Check if the script is running with admin rights
    if not is_admin():
        # If not, relaunch with admin rights
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{os.path.abspath(__file__)}"', None, 1)
            sys.exit(0)
        except Exception as e:
            print(f"Error elevating privileges: {e}")
            input("Press Enter to continue without admin privileges...")
    
    # Continue with admin rights
    create_gui()
