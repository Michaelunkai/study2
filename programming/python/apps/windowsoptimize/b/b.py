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
    
    Remove-Item -Path $env:TEMP\*, "$env:WINDIR\Temp\*", "$env:WINDIR\Prefetch\*", "C:\Users\*\AppData\Local\Temp\*" -Force -Recurse -ErrorAction SilentlyContinue
    try { cleanmgr /sageset:1 } catch { Write-Host "cleanmgr setup failed, continuing..." }
    try { cleanmgr /sagerun:1 } catch { Write-Host "cleanmgr run failed, continuing..." }
    try { cleanmgr /lowdisk } catch { Write-Host "cleanmgr lowdisk failed, continuing..." }
    
    # Clear recycle bin
    try {
        PowerShell -Command "Clear-RecycleBin -Force"
    } catch {
        Write-Host "Could not clear recycle bin, continuing..." -ForegroundColor Yellow
    }

    # System health checks
    try {
        Write-Host "Running system health checks..." -ForegroundColor Cyan
        Repair-WindowsImage -Online -ScanHealth
        Repair-WindowsImage -Online -RestoreHealth
        sfc /scannow
        DISM.exe /Online /Cleanup-Image /CheckHealth
        DISM.exe /Online /Cleanup-Image /RestoreHealth
        dism /online /cleanup-image /startcomponentcleanup
        dism /online /Cleanup-Image /AnalyzeComponentStore
        dism /online /Cleanup-Image /StartComponentCleanup /ResetBase
    } catch {
        Write-Host "Some system health checks failed, continuing..." -ForegroundColor Yellow
    }

    # Network reset
    try {
        Write-Host "Resetting network components..." -ForegroundColor Cyan
        netsh int ip reset
        ipconfig /release
        ipconfig /renew
        netsh winsock reset
        ipconfig /flushdns
    } catch {
        Write-Host "Network reset had issues, continuing..." -ForegroundColor Yellow
    }

    # Windows Update
    try {
        Write-Host "Working with Windows Updates..." -ForegroundColor Cyan
        net start wuauserv
        # Only try to install module if it doesn't exist
        if (-not (Get-Module -ListAvailable -Name PSWindowsUpdate)) {
            Install-Module -Name PSWindowsUpdate -Force -AllowClobber -Scope CurrentUser
        }
        Get-WindowsUpdate -Install -AcceptAll -Verbose
        Remove-Item -Path "C:\Windows\SoftwareDistribution\Download\*" -Force -Recurse -ErrorAction SilentlyContinue
    } catch {
        Write-Host "Windows Update operations had issues, continuing..." -ForegroundColor Yellow
    }

    # Disk optimization
    try {
        Write-Host "Optimizing disk..." -ForegroundColor Cyan
        defrag C: /U /V
        defrag /c /o
        Optimize-Volume -DriveLetter C -ReTrim -Confirm:$false -Verbose
        fsutil behavior set memoryusage 2
        compact.exe /CompactOS:always
    } catch {
        Write-Host "Some disk optimization operations failed, continuing..." -ForegroundColor Yellow
    }

    # Volume shadow copy cleanup
    try {
        vssadmin delete shadows /for=C: /all /quiet
        vssadmin delete shadows /for=C: /oldest
    } catch {
        Write-Host "Shadow copy cleanup had issues, continuing..." -ForegroundColor Yellow
    }

    # Run silent cleanup
    try {
        schtasks /Run /TN "\Microsoft\Windows\DiskCleanup\SilentCleanup"
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
    } catch {
        Write-Host "Event log clearing had issues, continuing..." -ForegroundColor Yellow
    }

    # File cleanups
    Write-Host "Cleaning system files..." -ForegroundColor Cyan
    del /q/f/s "C:\Windows\Logs\CBS\*"
    del /q/f/s "C:\Windows\Logs\DISM\*"
    del /q/f/s "C:\Windows\Logs\WindowsUpdate\*"
    del /q/f/s "C:\Windows\Prefetch\*"
    del /f /s /q "$env:LocalAppData\Microsoft\Windows\Explorer\thumbcache_*"
    del /q/f/s "C:\ProgramData\Microsoft\Windows\WER\*"
    del /q/f/s "$env:USERPROFILE\AppData\Local\Microsoft\Windows\Temporary Internet Files\*"
    del /q/f/s "C:\Windows\Logs\WMI\*.log"
    del /q/f/s "C:\Windows\SoftwareDistribution\DeliveryOptimization\*"
    del /q/f/s "$env:USERPROFILE\AppData\Local\Microsoft\Edge\User Data\Default\Cache\*"
    del /q/f/s "$env:USERPROFILE\AppData\Local\Microsoft\Edge\User Data\Default\Downloads\*"
    del /q/f/s "C:\ProgramData\Microsoft\Windows Defender\Scans\History\*"
    del /q/f/s "$env:USERPROFILE\AppData\Local\Microsoft\OneDrive\logs\*"
    del /q/f/s "$env:USERPROFILE\AppData\Local\Microsoft\Office\16.0\OfficeFileCache\*"
    del /q/f/s "C:\ProgramData\Microsoft\Windows\WER\ReportQueue\*"

    # Windows Store repair
    try {
        Write-Host "Repairing Windows Store..." -ForegroundColor Cyan
        Get-AppxPackage -allusers Microsoft.WindowsStore | ForEach-Object {
            Add-AppxPackage -register "$($_.InstallLocation)\appxmanifest.xml" -DisableDevelopmentMode
        }
    } catch {
        Write-Host "Windows Store repair failed, continuing..." -ForegroundColor Yellow
    }

    # Additional cleanups
    Remove-Item -Path "C:\Windows\Installer\$PatchCache$\*" -Force -Recurse -ErrorAction SilentlyContinue
    forfiles /p "C:\Windows\Temp" /s /m *.* /d -7 /c "cmd /c del @path" 2>$null

    # Network optimizations
    try {
        Write-Host "Optimizing network settings..." -ForegroundColor Cyan
        netsh int tcp set global autotuninglevel=normal
        netsh int tcp set global autotuninglevel=highlyrestricted
        netsh int tcp set global dca=enabled
        netsh int tcp set global ecncapability=enabled
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
            # We're already admin, run directly
            command = f'powershell.exe -ExecutionPolicy Bypass -File "{temp_file_path}"'
            status_text += f"Running command as admin: {command}\n"
            dpg.set_value("status_text", status_text)
            
            # Run the command and wait for completion
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Update status periodically while waiting for the process to complete
            while process.poll() is None:
                dpg.set_value("status_text", status_text + "PowerShell cleanup in progress...\n")
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
                status_text += "PowerShell system cleanup completed successfully!\n"
            else:
                status_text += f"PowerShell system cleanup exited with code {process.returncode}.\n"
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
    
    finally:
        # Clean up temporary file if we didn't need to elevate
        if is_admin() and 'temp_file_path' in locals():
            try:
                os.unlink(temp_file_path)
                status_text += "Temporary script file cleaned up.\n"
            except:
                status_text += "Could not delete temporary script file.\n"
            
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
    """Execute a specific PowerShell function by name"""
    status_text = f"Running PowerShell function: {function_name}...\n"
    dpg.set_value("status_text", status_text)
    
    try:
        # Execute PowerShell with the function name
        command = f'powershell.exe -ExecutionPolicy Bypass -Command "& {{ {function_name} }}"'
        status_text += f"Running command: {command}\n"
        dpg.set_value("status_text", status_text)
        
        # Run the command
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Update status while waiting
        while process.poll() is None:
            dpg.set_value("status_text", status_text + f"Function '{function_name}' in progress...\n")
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
            status_text += f"PowerShell function '{function_name}' completed successfully!\n"
        else:
            status_text += f"PowerShell function '{function_name}' exited with code {process.returncode}.\n"
            
    except Exception as e:
        status_text += f"Error executing PowerShell function: {str(e)}\n"
        status_text += traceback.format_exc() + "\n"
    
    # Update final status
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
    
    # Configure viewport
    dpg.create_viewport(title="Tools Launcher", width=800, height=550)  # Increased height for tabs
    dpg.set_viewport_resize_callback(lambda s, d: dpg.set_item_width("main_window", d[0]-20))
    
    # Set up the main window
    with dpg.window(tag="main_window", label="Tools Launcher", width=800, height=550, no_resize=True, no_close=True):
        dpg.add_spacer(height=10)
        
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=15)
            with dpg.group():  # Removed width parameter here
                dpg.add_text("Welcome to the Tools Launcher", color=[255, 255, 255])
                dpg.add_text("Use the tabs below to access different tool categories", color=[200, 200, 200])
                dpg.add_spacer(height=20)
                
                # Add tab bar - removed width parameter
                with dpg.tab_bar(tag="main_tabs"):
                    # Cleanup tab
                    with dpg.tab(label="Cleanup", tag="tab_cleanup"):
                        dpg.add_spacer(height=15)
                        
                        # First row of buttons
                        with dpg.group(horizontal=True):
                            dpg.add_spacer(width=25)
                            run_button = dpg.add_button(label="Run Tools", callback=run_tools_callback, width=200, height=60)
                            dpg.bind_item_theme(run_button, run_button_theme)
                            
                            dpg.add_spacer(width=20)
                            
                            close_button = dpg.add_button(label="Close Tools", callback=close_tools_callback, width=200, height=60)
                            dpg.bind_item_theme(close_button, close_button_theme)
                        
                        dpg.add_spacer(height=15)
                        
                        # PS1 clean button
                        with dpg.group(horizontal=True):
                            dpg.add_spacer(width=140)
                            ps1_button = dpg.add_button(
                                label="PS1 CLEAN", 
                                callback=run_ps1_clean_callback, 
                                width=200, 
                                height=60
                            )
                            dpg.bind_item_theme(ps1_button, ps1_button_theme)
                    
                    # After Format tab
                    with dpg.tab(label="After Format", tag="tab_after_format"):
                        dpg.add_spacer(height=15)
                        
                        # Description
                        with dpg.group(horizontal=True):
                            dpg.add_spacer(width=25)
                            dpg.add_text("Tools to use after a fresh Windows installation", color=[220, 220, 220])
                        
                        dpg.add_spacer(height=20)
                        
                        # PowerShell function buttons in a grid layout
                        ps_functions = [
                            "unlock", "update", "nvidia", "rewsl", 
                            "getcho", "g1337x", "vsc", "autocomplete", 
                            "cleanup", "get7z", "short2", "mas", 
                            "getarm", "fixtime", "getdirectx", "getvc", 
                            "rmgamebar", "getf4", "taskbar", "disadmin"
                        ]
                        
                        # Group for all buttons
                        with dpg.group():
                            # Create grid layout with 4 buttons per row
                            for i in range(0, len(ps_functions), 4):
                                with dpg.group(horizontal=True):
                                    dpg.add_spacer(width=25)
                                    for j in range(4):
                                        if i+j < len(ps_functions):
                                            function_name = ps_functions[i+j]
                                            button = dpg.add_button(
                                                label=function_name, 
                                                callback=lambda s, a, u: run_powershell_function(u),
                                                user_data=function_name,
                                                width=140,
                                                height=30
                                            )
                                            dpg.bind_item_theme(button, function_button_theme)
                                            dpg.add_spacer(width=10)
                                dpg.add_spacer(height=10)
                        
                        dpg.add_spacer(height=10)
                        
                        # Qaccess button (existing)
                        with dpg.group(horizontal=True):
                            dpg.add_spacer(width=140)
                            qaccess_button = dpg.add_button(
                                label="Qaccess", 
                                callback=qaccess_callback, 
                                width=200, 
                                height=60
                            )
                            dpg.bind_item_theme(qaccess_button, qaccess_button_theme)
                            
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

# Check if we need to run the PS clean script as admin
if len(sys.argv) > 1 and sys.argv[1] == "--ps-clean-admin":
    try:
        # Read the path to the temp file from the flag file
        flag_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "run_ps_clean.flag")
        if os.path.exists(flag_file):
            with open(flag_file) as f:
                temp_file_path = f.read().strip()
            
            if os.path.exists(temp_file_path):
                # Execute PowerShell script
                os.system(f'powershell.exe -ExecutionPolicy Bypass -File "{temp_file_path}"')
                # Clean up
                os.unlink(temp_file_path)
            
            # Remove flag file
            os.unlink(flag_file)
    except Exception as e:
        print(f"Error running admin cleanup: {e}")
        input("Press Enter to exit...")
    sys.exit()

if __name__ == "__main__":
    create_gui()
