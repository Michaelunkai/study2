import subprocess
import ctypes
import sys
import os
import winreg
import json

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTabWidget, QCheckBox,
    QPushButton, QLabel, QLineEdit, QHBoxLayout, QMessageBox, QFileDialog
)
from PyQt5.QtGui import QFont

# -----------------------------------------------------------
#                 Helper: Run Command as Admin
# -----------------------------------------------------------
def run_command_as_admin(command_or_list):
    """
    Runs the given PowerShell command with admin privileges.
    `command_or_list` can be a string or a list of arguments.
    """
    try:
        if sys.platform.startswith('win'):
            if ctypes.windll.shell32.IsUserAnAdmin() != 0:
                if isinstance(command_or_list, list):
                    subprocess.Popen(command_or_list, shell=True)
                else:
                    subprocess.Popen(["powershell", "-NoExit", "-Command", command_or_list], shell=True)
            else:
                if isinstance(command_or_list, list):
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


# -----------------------------------------------------------
#            Commands (Not Bulk / Bulk) Tabs
# -----------------------------------------------------------
def run_selected_commands():
    selected_commands = []
    for cmd, var in zip(commands, command_vars):
        if var.isChecked():
            selected_commands.append(
                f"Write-Host 'Running: {cmd['name']}'; {cmd['command']}; if ($?) {{ Write-Host 'Finished: {cmd['name']}' }} else {{ Write-Host 'Failed: {cmd['name']}' }}"
            )
    command_to_run = "; ".join(selected_commands)
    print("Running commands:", command_to_run)
    if command_to_run.strip():
        run_command_as_admin(command_to_run)
    else:
        QMessageBox.information(None, "No Commands", "No commands selected to run.")


# -----------------------------------------------------------
#                    System Info Button
# -----------------------------------------------------------
def run_sys_info():
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


# -----------------------------------------------------------
#             Choose All / Deselect All Buttons
# -----------------------------------------------------------
def choose_all():
    current_tab_index = tab_widget.currentIndex()
    if current_tab_index == 0:
        layout = not_bulk_layout
    elif current_tab_index == 1:
        layout = bulk_layout
    else:
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
    else:
        return
    for i in range(layout.count()):
        widget = layout.itemAt(i).widget()
        if isinstance(widget, QCheckBox):
            widget.setChecked(False)


# -----------------------------------------------------------
#                Startup Tab Functions
# -----------------------------------------------------------
def load_registry_startup_items():
    items = {}
    # Search additional keys including Wow6432Node for 32-bit apps on 64-bit systems.
    registry_keys = [
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\RunOnce"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\RunOnce"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Run"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Wow6432Node\Microsoft\Windows\CurrentVersion\RunOnce"),
    ]
    for hive, subkey in registry_keys:
        try:
            reg_key = winreg.OpenKey(hive, subkey, 0, winreg.KEY_READ)
            hive_name = "HKCU" if hive == winreg.HKEY_CURRENT_USER else "HKLM"
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
            pass
    return items

def load_startup_folder_items():
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

def load_wmi_startup_items():
    """Loads startup commands via the WMI class Win32_StartupCommand."""
    try:
        cmd = [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy", "Bypass",
            "-Command",
            "(Get-CimInstance -ClassName Win32_StartupCommand | Select-Object Name, Command, Location) | ConvertTo-Json -Compress"
        ]
        output = subprocess.check_output(cmd, universal_newlines=True, stderr=subprocess.STDOUT)
        if not output.strip():
            return {}
        items = json.loads(output)
        if isinstance(items, dict):
            items = [items]
        results = {}
        for item in items:
            key = f"WMI:{item.get('Name', 'Unknown')}"
            results[key] = {
                "source": "wmi",
                "name": item.get("Name", "Unknown"),
                "command": item.get("Command", ""),
                "location": item.get("Location", "")
            }
        return results
    except Exception as e:
        print("Error loading WMI startup items:", e)
        return {}

def load_all_startup_items():
    items = {}
    items.update(load_registry_startup_items())
    items.update(load_startup_folder_items())
    items.update(load_wmi_startup_items())
    return items

def is_protected_startup(item_data):
    protected_keywords = ['windows', 'microsoft', 'security', 'defender', 'antimalware', 'onedrive']
    text_to_check = ""
    if item_data["source"] == "registry":
        text_to_check = f"{item_data['name']} {item_data.get('value', '')}"
    elif item_data["source"] == "startup_folder":
        text_to_check = f"{item_data['name']} {item_data.get('path', '')}"
    elif item_data["source"] == "wmi":
        text_to_check = f"{item_data['name']} {item_data.get('command', '')} {item_data.get('location', '')}"
    for keyword in protected_keywords:
        if keyword in text_to_check.lower():
            return True
    return False

def disable_startup_item(item_key, item_data):
    reply = QMessageBox.question(
        None,
        "Confirm Disable",
        f"Are you sure you want to disable startup item '{item_data['name']}'?\nDisabling a critical item may cause issues.",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )
    if reply != QMessageBox.Yes:
        return
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
    elif item_data["source"] == "wmi":
        # For WMI startup items, we cannot disable them via this script.
        QMessageBox.information(None, "WMI Item", f"WMI startup item '{item_data['name']}' cannot be disabled via this tool.")
    refresh_startup_tab()

def add_startup_item():
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
    file_path, _ = QFileDialog.getOpenFileName(
        None, "Select Application", "", "Executable Files (*.exe);;All Files (*)"
    )
    if file_path:
        startup_command_input.setText(file_path)

def refresh_startup_tab():
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
        elif data["source"] == "startup_folder":
            folder_label = "User Startup" if data["folder_label"] == "UserStartup" else "All Users Startup"
            text = f"{folder_label}: {data['name']} -> {data['path']}"
        elif data["source"] == "wmi":
            text = f"WMI: {data['name']} -> {data.get('command', '')} (Location: {data.get('location', '')})"
        label = QLabel(text)
        if is_protected_startup(data):
            label.setStyleSheet("color: red;")
        disable_button = QPushButton("Disable")
        disable_button.clicked.connect(lambda checked, k=key, d=data: disable_startup_item(k, d))
        row.addWidget(label)
        row.addWidget(disable_button)
        container = QWidget()
        container.setLayout(row)
        startup_items_container.addWidget(container)


# -----------------------------------------------------------
#                  Main GUI Initialization
# -----------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    root = QWidget()
    root.setWindowTitle("Select Commands to Run")
    root.setStyleSheet("background-color: #f5f5dc;")
    root_layout = QVBoxLayout(root)

    # Create tab widget with three tabs: Not Bulk, Bulk, and Startup
    global tab_widget
    tab_widget = QTabWidget()
    root_layout.addWidget(tab_widget)

    tab_font = QFont("Lobster", 10, QFont.Bold)
    tab_widget.setFont(tab_font)

    # ------------------- Tab: Not Bulk -------------------
    not_bulk_tab = QWidget()
    global not_bulk_layout
    not_bulk_layout = QVBoxLayout()
    not_bulk_tab.setLayout(not_bulk_layout)
    tab_widget.addTab(not_bulk_tab, "Not Bulk")

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

    # ------------------- Tab: Startup -------------------
    startup_tab = QWidget()
    startup_layout = QVBoxLayout()
    startup_tab.setLayout(startup_layout)
    tab_widget.addTab(startup_tab, "Startup")

    global startup_items_container
    startup_items_container = QVBoxLayout()
    startup_layout.addLayout(startup_items_container)

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

    # ------------------- Checkbox Setup -------------------
    global command_vars
    command_vars = []

    # Define bulk_commands globally before use
    global bulk_commands
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

    global commands
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

    for cmd in commands:
        checkbox = QCheckBox(cmd['name'], parent=root)
        checkbox.setFont(QFont("Lobster", 10, QFont.Bold))
        command_vars.append(checkbox)
        if cmd["name"] in bulk_commands:
            bulk_layout.addWidget(checkbox)
        else:
            not_bulk_layout.addWidget(checkbox)

    choose_all_button = QPushButton("Choose All", parent=root)
    choose_all_button.clicked.connect(choose_all)
    choose_all_button.setStyleSheet("background-color: black; color: white; font-weight: bold;")
    root_layout.addWidget(choose_all_button)

    deselect_all_button = QPushButton("Deselect All", parent=root)
    deselect_all_button.clicked.connect(deselect_all)
    deselect_all_button.setStyleSheet("background-color: black; color: white; font-weight: bold;")
    root_layout.addWidget(deselect_all_button)

    run_button = QPushButton("Run Selected Commands", parent=root)
    run_button.clicked.connect(run_selected_commands)
    run_button.setStyleSheet("background-color: black; color: white; font-weight: bold;")
    root_layout.addWidget(run_button)

    root.setLayout(root_layout)
    root.showMaximized()

    sys.exit(app.exec_())
