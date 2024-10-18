import subprocess
import ctypes
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QCheckBox, QPushButton, QLabel
from PyQt5.QtGui import QFont

def run_command_as_admin(command):
    try:
        if sys.platform.startswith('win'):
            if ctypes.windll.shell32.IsUserAnAdmin() != 0:
                subprocess.Popen(["powershell", "-NoExit", "-Command", command], shell=True)
            else:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", "powershell", f"-NoExit -Command {command}", None, 1)
    except Exception as e:
        print("Error:", e)

def run_selected_commands():
    selected_commands = []
    for cmd, var in zip(commands, command_vars):
        if var.isChecked():
            selected_commands.append(f"Write-Host 'Running: {cmd['name']}'; {cmd['command']}; if ($?) {{ Write-Host 'Finished: {cmd['name']}' }} else {{ Write-Host 'Failed: {cmd['name']}' }}")
    
    command_to_run = "; ".join(selected_commands)
    print("Running commands:", command_to_run)  # Debugging statement
    run_command_as_admin(command_to_run)

def choose_all():
    current_tab_index = tab_widget.currentIndex()
    if current_tab_index == 0:
        layout = not_bulk_layout
    elif current_tab_index == 1:
        layout = bulk_layout
    else:
        layout = wsl2_layout

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
        layout = wsl2_layout

    for i in range(layout.count()):
        widget = layout.itemAt(i).widget()
        if isinstance(widget, QCheckBox):
            widget.setChecked(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    root = QWidget()
    root.setWindowTitle("Select Commands to Run")
    root.setStyleSheet("background-color: #f5f5dc;")

    tab_widget = QTabWidget()
    root_layout = QVBoxLayout(root)
    root_layout.addWidget(tab_widget)

    # Set font for tab titles
    tab_font = QFont("Lobster", 10, QFont.Bold)
    tab_widget.setFont(tab_font)

    # Initialize tabs for different commands
    not_bulk_tab = QWidget()
    not_bulk_layout = QVBoxLayout()
    not_bulk_tab.setLayout(not_bulk_layout)
    tab_widget.addTab(not_bulk_tab, "Not Bulk")

    bulk_tab = QWidget()
    bulk_layout = QVBoxLayout()
    bulk_tab.setLayout(bulk_layout)
    tab_widget.addTab(bulk_tab, "Bulk")

    # Create a new tab for WSL2 specific commands
    wsl2_tab = QWidget()
    wsl2_layout = QVBoxLayout()
    wsl2_tab.setLayout(wsl2_layout)
    tab_widget.addTab(wsl2_tab, "WSL2")

    command_vars = []
    wsl2_commands = ["Unregister Kali WSL", "Import Kali WSL", "Unregister Ubuntu WSL", "Import Ubuntu WSL"]

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
