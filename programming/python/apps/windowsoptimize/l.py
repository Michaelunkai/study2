import subprocess
import ctypes
import sys
import os
import winreg
import json

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTabWidget, QCheckBox,
    QPushButton, QLabel, QLineEdit, QHBoxLayout, QMessageBox, QFileDialog, QScrollArea
)
from PyQt5.QtGui import QFont

# ------------------- Common Admin Command Runner -------------------
def run_command_as_admin(command_or_list):
    """
    Runs the given PowerShell command with admin privileges.
    `command_or_list` can be a string or a list of arguments.
    """
    try:
        if sys.platform.startswith('win'):
            # If the user is already elevated, run directly.
            # Otherwise, we elevate using ShellExecuteW with "runas".
            if ctypes.windll.shell32.IsUserAnAdmin() != 0:
                if isinstance(command_or_list, list):
                    subprocess.Popen(command_or_list, shell=True)
                else:
                    subprocess.Popen(["powershell", "-NoExit", "-Command", command_or_list], shell=True)
            else:
                # We must convert a list into a single string if needed
                if isinstance(command_or_list, list):
                    # Escape each argument with quotes if needed
                    cmd_str = " ".join(f"'{arg}'" if " " in arg else arg for arg in command_or_list)
                    ctypes.windll.shell32.ShellExecuteW(
                        None, "runas", "powershell",
                        f"-NoExit -Command {cmd_str}", None, 1
                    )
                else:
                    ctypes.windll.shell32.ShellExecuteW(
                        None, "runas", "powershell",
                        f"-NoExit -Command {command_or_list}", None, 1
                    )
    except Exception as e:
        print("Error:", e)

# ------------------- Commands Checkboxes: Bulk, WSL2, Not Bulk -------------------
def run_selected_commands():
    """
    Gathers all checked commands from the three checkbox tabs (Not Bulk, Bulk, WSL2)
    and runs them in a single PowerShell session with admin privileges.
    """
    selected_commands = []
    for cmd, var in zip(commands, command_vars):
        if var.isChecked():
            # Wrap each command with status messages for clarity
            selected_commands.append(
                f"Write-Host 'Running: {cmd['name']}'; {cmd['command']}; if ($?) {{ Write-Host 'Finished: {cmd['name']}' }} else {{ Write-Host 'Failed: {cmd['name']}' }}"
            )
    command_to_run = "; ".join(selected_commands)
    print("Running commands:", command_to_run)
    if command_to_run.strip():
        run_command_as_admin(command_to_run)
    else:
        QMessageBox.information(None, "No Commands", "No commands selected to run.")

# ------------------- System Info Button -------------------
def run_sys_info():
    """
    Runs a comprehensive system info one-liner in PowerShell as admin.
    Displays CPU, GPU, RAM usage, OS info, motherboard, etc.
    """
    sys_info_command = (
        "$cs=Get-CimInstance Win32_ComputerSystem; "
        "$os=Get-CimInstance Win32_OperatingSystem; "
        "$cpu=Get-CimInstance Win32_Processor; "
        "$gpu=Get-CimInstance Win32_VideoController; "
        "$bios=Get-CimInstance Win32_BIOS; "
        "$disk=(Get-CimInstance Win32_LogicalDisk -Filter \"DriveType=3\"|Measure-Object -Property Size,FreeSpace -Sum); "
        "$pdisk=Get-PhysicalDisk|Select-Object -First 1; "
        "$mb=Get-CimInstance Win32_BaseBoard; "
        "$ramUsage=(Get-Counter '\\Memory\\% Committed Bytes In Use').CounterSamples.CookedValue; "
        "$cpuUsage=(Get-Counter '\\Processor(_Total)\\% Processor Time').CounterSamples.CookedValue; "
        "$gpuUsage=(Get-Counter '\\GPU Engine(*engtype_3D)\\Utilization Percentage' -ErrorAction SilentlyContinue).CounterSamples|Measure-Object -Property CookedValue -Average; "
        "[PSCustomObject]@{GPU=$gpu.VideoProcessor;CPU=$cpu.Name;CPU_Speed_GHz=$cpu.MaxClockSpeed/1000;RAM_GB=[math]::Round($cs.TotalPhysicalMemory/1GB,2);"
        "RAM_Used_Percent=[math]::Round($ramUsage,2);CPU_Used_Percent=[math]::Round($cpuUsage,2);"
        "GPU_Used_Percent=if($gpuUsage.Average){[math]::Round($gpuUsage.Average,2)}else{'N/A'};"
        "OS=$os.Caption;OS_Version=$os.Version;Model=$cs.Model;SerialNumber=$bios.SerialNumber;"
        "StorageType=$pdisk.MediaType;Storage_Capacity_GB=[math]::Round($disk.SumSize/1GB,2);"
        "Storage_Free_GB=[math]::Round($disk.SumFreeSpace/1GB,2);Motherboard=$mb.Product;"
        "MotherboardManufacturer=$mb.Manufacturer} | Format-List"
    )
    run_command_as_admin(sys_info_command)

# ------------------- "Choose All" and "Deselect All" Buttons -------------------
def choose_all():
    current_tab_index = tab_widget.currentIndex()
    if current_tab_index == 0:
        layout = not_bulk_layout
    elif current_tab_index == 1:
        layout = bulk_layout
    elif current_tab_index == 2:
        layout = wsl2_layout
    else:
        # "Startup" tab index is 3, "Uninstall" is 4
        # These tabs don't use checkboxes, so do nothing.
        return

    for i in range(layout.count()):
        widget = layout.itemAt(i).widget()
        if isinstance(widget, QCheckBox):
            widget.setChecked(True)

def deselect_all():
    current_tab_index = tab_widget.currentIndex()
    if current_tab_index == 0:
        layout = not_bulk_layout
    elif current_tab_index == 1:
        layout = bulk_layout
    elif current_tab_index == 2:
        layout = wsl2_layout
    else:
        return

    for i in range(layout.count()):
        widget = layout.itemAt(i).widget()
        if isinstance(widget, QCheckBox):
            widget.setChecked(False)

# ------------------- Startup Tab Functions -------------------
def load_registry_startup_items():
    """
    Reads startup items from HKCU and HKLM in "Run" and "RunOnce" keys.
    Returns a dict with keys like "HKCU:appname" -> metadata.
    """
    items = {}
    for hive, hive_name in [(winreg.HKEY_CURRENT_USER, "HKCU"), (winreg.HKEY_LOCAL_MACHINE, "HKLM")]:
        for subkey in [r"Software\Microsoft\Windows\CurrentVersion\Run", r"Software\Microsoft\Windows\CurrentVersion\RunOnce"]:
            try:
                reg_key = winreg.OpenKey(hive, subkey, 0, winreg.KEY_READ)
                i = 0
                while True:
                    try:
                        name, value, _ = winreg.EnumValue(reg_key, i)
                        key_id = f"{hive_name}:{name}"
                        items[key_id] = {
                            "source": "registry",
                            "hive": hive,
                            "hive_name": hive_name,
                            "key": subkey,
                            "name": name,
                            "value": value
                        }
                        i += 1
                    except OSError:
                        break
                winreg.CloseKey(reg_key)
            except Exception:
                # If the key doesn't exist or can't be opened, skip.
                pass
    return items

def load_startup_folder_items():
    """
    Reads items (shortcuts, scripts, etc.) from the current user's
    and All Users' Startup folders.
    """
    items = {}
    user_startup = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    all_users_startup = os.path.join(os.getenv("PROGRAMDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    for folder, folder_label in [(user_startup, "UserStartup"), (all_users_startup, "AllUsersStartup")]:
        if not folder or not os.path.isdir(folder):
            continue
        try:
            for item in os.listdir(folder):
                full_path = os.path.join(folder, item)
                key_id = f"{folder_label}:{item}"
                items[key_id] = {
                    "source": "startup_folder",
                    "folder": folder,
                    "folder_label": folder_label,
                    "name": item,
                    "path": full_path
                }
        except Exception:
            pass
    return items

def load_all_startup_items():
    """
    Combines registry and startup folder items into a single dictionary.
    """
    items = {}
    items.update(load_registry_startup_items())
    items.update(load_startup_folder_items())
    return items

def is_protected_startup(item_data):
    """
    Determines if an item is "protected" by searching for specific keywords
    in the name or path. Protected items are displayed in red and cannot be disabled.
    """
    protected_keywords = ['windows', 'microsoft', 'security', 'defender', 'antimalware', 'onedrive']
    text_to_check = ""
    if item_data["source"] == "registry":
        text_to_check = f"{item_data['name']} {item_data.get('value', '')}"
    else:
        text_to_check = f"{item_data['name']} {item_data.get('path', '')}"
    for keyword in protected_keywords:
        if keyword in text_to_check.lower():
            return True
    return False

def disable_startup_item(item_key, item_data):
    """
    Removes the startup entry from registry or deletes the file from the Startup folder.
    """
    if item_data["source"] == "registry":
        try:
            reg_key = winreg.OpenKey(item_data["hive"], item_data["key"], 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(reg_key, item_data["name"])
            winreg.CloseKey(reg_key)
            QMessageBox.information(None, "Startup", f"Disabled registry startup item: {item_data['name']}")
        except Exception as e:
            QMessageBox.warning(None, "Error", f"Error disabling {item_data['name']}: {e}")
    elif item_data["source"] == "startup_folder":
        try:
            os.remove(item_data["path"])
            QMessageBox.information(None, "Startup", f"Disabled startup folder item: {item_data['name']}")
        except Exception as e:
            QMessageBox.warning(None, "Error", f"Error disabling {item_data['name']}: {e}")
    refresh_startup_tab()

def add_startup_item():
    """
    Adds a new startup entry to the HKCU Run registry key.
    The user can supply a name and a path to an exe or script.
    """
    name = startup_name_input.text().strip()
    command = startup_command_input.text().strip()
    if not name or not command:
        QMessageBox.warning(None, "Input Error", "Both name and command must be provided.")
        return
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"Software\Microsoft\Windows\CurrentVersion\Run",
                                 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(reg_key, name, 0, winreg.REG_SZ, command)
        winreg.CloseKey(reg_key)
        QMessageBox.information(None, "Startup", f"Added startup item: {name}")
    except Exception as e:
        QMessageBox.warning(None, "Error", f"Error adding startup item {name}: {e}")
    startup_name_input.clear()
    startup_command_input.clear()
    refresh_startup_tab()

def browse_startup_app():
    """
    Opens a file dialog to pick an executable, then populates the command field.
    """
    file_path, _ = QFileDialog.getOpenFileName(
        None, "Select Application", "", "Executable Files (*.exe);;All Files (*)"
    )
    if file_path:
        startup_command_input.setText(file_path)

def refresh_startup_tab():
    """
    Clears the startup items layout and rebuilds it with the latest data.
    """
    count = startup_items_container.count()
    for i in reversed(range(count)):
        item = startup_items_container.takeAt(i)
        if item.widget():
            item.widget().deleteLater()
    
    all_items = load_all_startup_items()
    for key, data in all_items.items():
        row = QHBoxLayout()
        if data["source"] == "registry":
            text = (f"Registry ({data['hive_name']}): {data['name']} -> {data['value']} "
                    f"(Key: {data['key']})")
        else:
            folder_label = "User Startup" if data["folder_label"] == "UserStartup" else "All Users Startup"
            text = f"{folder_label}: {data['name']} -> {data['path']}"
        label = QLabel(text)
        
        # If it's "protected", highlight in red and disable the "Disable" button
        if is_protected_startup(data):
            label.setStyleSheet("color: red;")
        
        disable_button = QPushButton("Disable")
        if is_protected_startup(data):
            disable_button.setEnabled(False)
        else:
            disable_button.clicked.connect(lambda checked, k=key, d=data: disable_startup_item(k, d))
        
        row.addWidget(label)
        row.addWidget(disable_button)
        
        container = QWidget()
        container.setLayout(row)
        startup_items_container.addWidget(container)

# ------------------- Uninstall Tab Functions -------------------
def load_installed_apps():
    """
    Uses PowerShell to list installed UWP apps for all users, returning JSON.
    We parse the JSON to get a list of dicts with keys "Name" and "PackageFullName".
    """
    try:
        cmd = [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy", "Bypass",
            "-Command",
            "(Get-AppxPackage -AllUsers | Select-Object Name, PackageFullName) | ConvertTo-Json -Compress"
        ]
        output = subprocess.check_output(cmd, universal_newlines=True, stderr=subprocess.STDOUT)
        
        # If output is empty or whitespace, no apps found
        if not output.strip():
            return []
        
        apps = json.loads(output)
        # If there's only one item, PowerShell returns a dict
        if isinstance(apps, dict):
            apps = [apps]
        return apps
    except subprocess.CalledProcessError as cpe:
        # Non-zero exit code from PowerShell
        QMessageBox.warning(None, "Error", f"Error loading installed apps (exit code {cpe.returncode}):\n{cpe.output}")
        return []
    except Exception as e:
        QMessageBox.warning(None, "Error", f"Error loading installed apps: {e}")
        return []

def uninstall_app(package_full_name, app_name):
    """
    Prompts for confirmation, then uninstalls the UWP package
    and attempts to remove leftover provisioned package data.
    """
    reply = QMessageBox.question(
        None,
        "Confirm Uninstall",
        f"Are you sure you want to uninstall '{app_name}'?\nThis may remove all leftovers.",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )
    if reply == QMessageBox.Yes:
        try:
            # We call run_command_as_admin to ensure we have privileges
            cmd = [
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy", "Bypass",
                "-Command",
                (
                    f"Get-AppxPackage -PackageFullName '{package_full_name}' "
                    f"| Remove-AppxPackage -ErrorAction SilentlyContinue; "
                    f"$pkg = Get-AppxPackage -PackageFullName '{package_full_name}' "
                    f"-ErrorAction SilentlyContinue; "
                    f"Remove-AppxProvisionedPackage -Online "
                    f"-PackageName $pkg.PackageFamilyName -ErrorAction SilentlyContinue;"
                )
            ]
            run_command_as_admin(cmd)
            QMessageBox.information(None, "Uninstall", f"Uninstall initiated for '{app_name}'.")
            refresh_uninstall_tab()
        except Exception as e:
            QMessageBox.warning(None, "Error", f"Error uninstalling '{app_name}': {e}")

def refresh_uninstall_tab():
    """
    Rebuilds the uninstall tab layout by listing installed UWP apps
    and creating "Uninstall" buttons for each.
    """
    count = uninstall_items_container.count()
    for i in reversed(range(count)):
        item = uninstall_items_container.takeAt(i)
        if item.widget():
            item.widget().deleteLater()
    
    apps = load_installed_apps()
    for app in apps:
        row = QHBoxLayout()
        app_name = app.get("Name", "Unknown")
        package_full_name = app.get("PackageFullName", "")
        
        label = QLabel(f"{app_name} ({package_full_name})")
        uninstall_button = QPushButton("Uninstall")
        uninstall_button.clicked.connect(
            lambda checked, pfn=package_full_name, name=app_name: uninstall_app(pfn, name)
        )
        
        row.addWidget(label)
        row.addWidget(uninstall_button)
        
        container = QWidget()
        container.setLayout(row)
        uninstall_items_container.addWidget(container)

def refresh_installed_apps():
    """
    Public function to manually trigger a refresh of the uninstall tab list.
    """
    refresh_uninstall_tab()

# ------------------- Main GUI Initialization -------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    root = QWidget()
    root.setWindowTitle("Select Commands to Run")
    root.setStyleSheet("background-color: #f5f5dc;")
    root_layout = QVBoxLayout(root)
    
    # Create tab widget
    global tab_widget
    tab_widget = QTabWidget()
    root_layout.addWidget(tab_widget)
    
    # Set custom font for tab titles
    tab_font = QFont("Lobster", 10, QFont.Bold)
    tab_widget.setFont(tab_font)
    
    # ------------------- Tab: Not Bulk -------------------
    not_bulk_tab = QWidget()
    global not_bulk_layout
    not_bulk_layout = QVBoxLayout()
    not_bulk_tab.setLayout(not_bulk_layout)
    tab_widget.addTab(not_bulk_tab, "Not Bulk")
    
    # "SyS INFO" button in Not Bulk tab
    sys_info_button = QPushButton("SyS INFO", parent=root)
    sys_info_button.setStyleSheet("background-color: black; color: white; font-weight: bold;")
    sys_info_button.clicked.connect(run_sys_info)
    not_bulk_layout.addWidget(sys_info_button)
    
    # ------------------- Tab: Bulk -------------------
    bulk_tab = QWidget()
    global bulk_layout
    bulk_layout = QVBoxLayout()
    bulk_tab.setLayout(bulk_layout)
    tab_widget.addTab(bulk_tab, "Bulk")
    
    # ------------------- Tab: WSL2 -------------------
    wsl2_tab = QWidget()
    global wsl2_layout
    wsl2_layout = QVBoxLayout()
    wsl2_tab.setLayout(wsl2_layout)
    tab_widget.addTab(wsl2_tab, "WSL2")
    
    # ------------------- Tab: Startup -------------------
    startup_tab = QWidget()
    startup_layout = QVBoxLayout()
    startup_tab.setLayout(startup_layout)
    tab_widget.addTab(startup_tab, "Startup")
    
    global startup_items_container
    startup_items_container = QVBoxLayout()
    startup_layout.addLayout(startup_items_container)
    
    # "Add Startup Item" section
    add_startup_container = QHBoxLayout()
    global startup_name_input
    startup_name_input = QLineEdit()
    startup_name_input.setPlaceholderText("Startup Name")
    global startup_command_input
    startup_command_input = QLineEdit()
    startup_command_input.setPlaceholderText("Command/Path")
    
    browse_button = QPushButton("Browse")
    browse_button.clicked.connect(browse_startup_app)
    
    add_startup_button = QPushButton("Add Startup Item")
    add_startup_button.clicked.connect(add_startup_item)
    
    add_startup_container.addWidget(startup_name_input)
    add_startup_container.addWidget(startup_command_input)
    add_startup_container.addWidget(browse_button)
    add_startup_container.addWidget(add_startup_button)
    
    startup_layout.addLayout(add_startup_container)
    refresh_startup_tab()
    
    # ------------------- Tab: Uninstall -------------------
    uninstall_tab = QWidget()
    uninstall_layout = QVBoxLayout()
    uninstall_tab.setLayout(uninstall_layout)
    tab_widget.addTab(uninstall_tab, "Uninstall")
    
    # Scroll area for listing many installed apps
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    uninstall_items_widget = QWidget()
    global uninstall_items_container
    uninstall_items_container = QVBoxLayout(uninstall_items_widget)
    scroll.setWidget(uninstall_items_widget)
    uninstall_layout.addWidget(scroll)
    
    # Initial load of installed apps
    refresh_installed_apps()
    
    # ------------------- Checkbox Setup -------------------
    global command_vars
    command_vars = []
    
    wsl2_commands = ["Unregister Kali WSL", "Import Kali WSL", "Unregister Ubuntu WSL", "Import Ubuntu WSL"]
    
    # The list of commands used for Not Bulk / Bulk / WSL2
    commands = [
        {"name": "Update choco Packages", "command": "choco upgrade all -y --force"},
        {"name": "Scan System Health", "command": "Repair-WindowsImage -Online -ScanHealth"},
        {"name": "Restore System Health", "command": "Repair-WindowsImage -Online -RestoreHealth"},
        {"name": "Check System Files", "command": "sfc /scannow"},
        {"name": "Check Image Health", "command": "DISM.exe /Online /Cleanup-Image /CheckHealth"},
        {"name": "Restore Image Health", "command": "DISM.exe /Online /Cleanup-Image /RestoreHealth"},
        {"name": "Cleanup Component Store", "command": "dism /online /cleanup-image /startcomponentcleanup"},
        {"name": "Check Disk Errors", "command": "chkdsk /f /r"},
        {"name": "Start Update Service", "command": "net start wuauserv"},
        {"name": "windows updates", "command": "Install-Module -Name PSWindowsUpdate -Force -AllowClobber -Scope CurrentUser; Get-WindowsUpdate -Install -AcceptAll -Verbose"},
        {"name": "Defragment C Drive", "command": "defrag C: /U /V"},
        {"name": "Reset TCP/IP Stack", "command": "netsh int ip reset"},
        {"name": "Reset/Renew IP", "command": "ipconfig /release; ipconfig /renew"},
        {"name": "Reset Winsock", "command": "netsh winsock reset"},
        {"name": "Analyze Component Store", "command": "dism /online /cleanup-image /analyzecomponentstore"},
        {"name": "Cleanup Component Store", "command": "dism /online /cleanup-image /startcomponentcleanup"},
        {"name": "Flush DNS Cache", "command": "ipconfig /flushdns"},
        {"name": "Clear Application Log", "command": "wevtutil cl Application"},
        {"name": "Clear Security Log", "command": "wevtutil cl Security"},
        {"name": "Clear System Log", "command": "wevtutil cl System"},
        {"name": "Clear DNS Cache", "command": "Clear-DnsClientCache"},
        {"name": "Reinstall Microsoft Store", "command": "Get-AppxPackage -allusers Microsoft.WindowsStore | foreach {Add-AppxPackage -register \"$($_.InstallLocation)\\appxmanifest.xml\" -DisableDevelopmentMode}"},
        {"name": "Unregister Kali WSL", "command": "wsl --unregister kali-linux"},
        {"name": "Import Kali WSL", "command": "wsl --import kali-linux C:\\wsl2 C:\\backup\\linux\\wsl\\kalifull.tar"},
        {"name": "Unregister Ubuntu WSL", "command": "wsl --unregister ubuntu"},
        {"name": "Import Ubuntu WSL", "command": "wsl --import ubuntu C:\\wsl2\\ubuntu\\ C:\\backup\\linux\\wsl\\ubuntu.tar"},
        {"name": "Export WSL2 Distros", "command": "wsl --export kali-linux C:\\backup\\linux\\kalifull.tar; wsl --export ubuntu C:\\backup\\linux\\ubuntu.tar"},
        {"name": "Turbo Mod", "command": "python C:\\backup\\windowsapps\\powerplans\\turbo.py"},
        {"name": "PowerSaving Mod", "command": "python C:\\backup\\windowsapps\\powerplans\\powersavings.py"},
        {"name": "Enable SSH", "command": "Add-WindowsCapability -Online -Name OpenSSH.Server; Start-Service sshd; Set-Service -Name sshd -StartupType 'Automatic'; New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22; Get-Service sshd"},
        {"name": "Ram Usage", "command": "$totalMemory = (Get-WmiObject Win32_ComputerSystem).TotalPhysicalMemory; Get-Process | Sort-Object -Property WorkingSet -Descending | Select-Object Name, @{Name='MemoryUsage(MB)'; Expression={[math]::Round($_.WorkingSet / 1MB, 2)}}, @{Name='MemoryUsage(%)'; Expression={($_.WorkingSet / $totalMemory) * 100}}"},
        {"name": "cleanmgr Tool", "command": "cleanmgr /sageset:1"},
        {"name": "Delete TEMP folders", "command": "Remove-Item -Path $env:TEMP\\*,$env:WINDIR\\Temp\\*,$env:WINDIR\\Prefetch\\*,\"C:\\Users\\*\\AppData\\Local\\Temp\\*\" -Force -Recurse -ErrorAction SilentlyContinue"},
        {"name": "Clear Event Logs", "command": "wevtutil cl Application; wevtutil cl Security; wevtutil cl System"},
        {"name": "Compact Windows Installation", "command": "compact.exe /CompactOS:always"},
        {"name": "Remove Restore Points", "command": "vssadmin delete shadows /for=c: /all /quiet"},
        {"name": "Uninstall Pre-installed Bloatware", "command": "Get-AppxPackage -AllUsers | Remove-AppxPackage"},
        {"name": "Disable All Startup Programs", "command": 'Get-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" | ForEach-Object { Remove-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" -Name $_.PSObject.Properties.Name; Write-Output "Disabled startup program: $($_.PSObject.Properties.Name)" }; Get-CimInstance -ClassName Win32_StartupCommand | ForEach-Object { $_ | Invoke-CimMethod -MethodName Disable; Write-Output "Disabled startup program in Task Manager: $($_.Name)" }'},
        {"name": "Energy Report", "command": "powercfg -energy"},
        {"name": "Memory Diagnostic", "command": "mdsched"},
        {"name": "Performance Monitor", "command": "perfmon /report"},
        {"name": "System Config", "command": "msconfig"},
        {"name": "Malicious Software Removal", "command": "mrt"},
        {"name": "System Properties", "command": "sysdm.cpl"},
        {"name": "Remove Bloatware 2", "command": "Get-AppxPackage | Remove-AppxPackage"},
        {"name": "Optimize Disk Caching", "command": "fsutil behavior set memoryusage 2"},
        {"name": "Enable TCP Window Scaling", "command": "netsh int tcp set global autotuninglevel=normal"},
        {"name": "Reclaim Unused Space", "command": "Optimize-Volume -DriveLetter C -ReTrim -Verbose"},
        {"name": "Optimize TCP Network Performance", "command": "netsh int tcp set global autotuninglevel=highlyrestricted"},
        {"name": "Enable Direct Cache Access (DCA)", "command": "netsh int tcp set global dca=enabled"},
        {"name": "Explicit Congestion Notification (ECN) Capability", "command": "netsh int tcp set global ecncapability=enabled"},
        {"name": "Cleaning Up Low Disk Space", "command": "cleanmgr /lowdisk"},
        {"name": "Disable Firewall", "command": "Set-NetFirewallProfile -Profile Domain, Private, Public -Enabled False"},
        {"name": "Enable Firewall", "command": "Set-NetFirewallProfile -Profile Domain, Private, Public -Enabled True"},
    ]
    
    # Identify which commands go to which tab
    bulk_commands = [
        "Update choco Packages", "Scan System Health", "Restore System Health", "Check System Files",
        "Check Image Health", "Restore Image Health", "Cleanup Component Store", "Start Update Service",
        "windows updates", "Defragment C Drive", "Reset TCP/IP Stack", "Reset Winsock", "Analyze Component Store",
        "Cleanup Component Store", "Flush DNS Cache", "Clear Application Log", "Clear Security Log", "Clear System Log",
        "Clear DNS Cache", "Quick Scan", "Full Scan", "Reset/Renew IP", "cleanmgr Tool", "Delete TEMP folders",
        "Clear Event Logs", "Compact Windows Installation", "Optimize Disk Caching", "Enable TCP Window Scaling",
        "Reclaim Unused Space", "Optimize TCP Network Performance", "Cleaning Up Low Disk Space",
        "Reset TCP/IP Stack", "Reset/Renew IP", "Reset Winsock", "Flush DNS Cache", "Clear DNS Cache", 
        "Enable TCP Window Scaling", "Optimize TCP Network Performance", "Enable Direct Cache Access (DCA)", 
        "Explicit Congestion Notification (ECN) Capability"
    ]
    
    for cmd in commands:
        checkbox = QCheckBox(cmd['name'], parent=root)
        checkbox.setFont(QFont("Lobster", 10, QFont.Bold))
        command_vars.append(checkbox)
        
        if cmd["name"] in bulk_commands:
            bulk_layout.addWidget(checkbox)
        elif cmd["name"] in wsl2_commands:
            wsl2_layout.addWidget(checkbox)
        else:
            not_bulk_layout.addWidget(checkbox)
    
    # "Choose All" and "Deselect All" buttons at the bottom
    choose_all_button = QPushButton("Choose All", parent=root)
    choose_all_button.clicked.connect(choose_all)
    choose_all_button.setStyleSheet("background-color: black; color: white; font-weight: bold;")
    root_layout.addWidget(choose_all_button)
    
    deselect_all_button = QPushButton("Deselect All", parent=root)
    deselect_all_button.clicked.connect(deselect_all)
    deselect_all_button.setStyleSheet("background-color: black; color: white; font-weight: bold;")
    root_layout.addWidget(deselect_all_button)
    
    # "Run Selected Commands" button
    run_button = QPushButton("Run Selected Commands", parent=root)
    run_button.clicked.connect(run_selected_commands)
    run_button.setStyleSheet("background-color: black; color: white; font-weight: bold;")
    root_layout.addWidget(run_button)
    
    root.setLayout(root_layout)
    root.showMaximized()
    
    sys.exit(app.exec_())
