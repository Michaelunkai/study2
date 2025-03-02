import os
import subprocess
import tkinter as tk
from tkinter import ttk
import win32com.client  # pip install pywin32

# Global list to track processes launched by shortcuts
launched_processes = []

# ---------------------------
# Helper Functions to Run PowerShell
# ---------------------------
def run_ps_individual(cmd):
    """
    Launch a single PowerShell command in a new window.
    """
    try:
        subprocess.Popen(
            f'start powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "{cmd}"',
            shell=True
        )
    except Exception as e:
        print(f"Error running PowerShell command: {e}")

def run_ps_all(commands):
    """
    Combine a list of PowerShell command strings into one script and run them sequentially
    in a single PowerShell window (with -NoExit so you can see the output).
    """
    combined = " ; ".join(commands)
    try:
        subprocess.Popen(
            f'start powershell.exe -NoExit -NoProfile -ExecutionPolicy Bypass -Command "{combined}"',
            shell=True
        )
    except Exception as e:
        print(f"Error running combined PowerShell commands: {e}")

# ---------------------------
# Shortcuts Functions (Tab 1)
# ---------------------------
def find_all_shortcuts(root_dir):
    """
    Recursively search for every .lnk file under root_dir.
    Returns a list of tuples: (display_name, full_path).
    """
    shortcuts = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(".lnk"):
                full_path = os.path.join(dirpath, filename)
                shortcuts.append((filename, full_path))
    return shortcuts

def launch_shortcut(shortcut_path):
    """
    Uses WScript.Shell to read and launch the target of a Windows shortcut.
    """
    try:
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(shortcut_path)
        target = shortcut.TargetPath
        arguments = shortcut.Arguments
        if arguments:
            proc = subprocess.Popen([target] + arguments.split(), shell=False)
        else:
            proc = subprocess.Popen([target], shell=False)
        launched_processes.append(proc)
    except Exception as e:
        print(f"Error launching shortcut {shortcut_path}: {e}")

def close_all_apps():
    """
    Terminates every process launched via shortcuts and force-kills known maintenance apps.
    """
    global launched_processes
    for proc in launched_processes:
        try:
            proc.terminate()
        except Exception as e:
            print(f"Error terminating process: {e}")
    launched_processes = []
    # Force-kill known apps (adjust process names if needed)
    for proc_name in ["ccleaner.exe", "asc.exe"]:
        try:
            subprocess.Popen(f'taskkill /im {proc_name} /f', shell=True)
        except Exception as e:
            print(f"Error killing process {proc_name}: {e}")

# ---------------------------
# WinOptimize Command Definitions (Tab 2)
# Each tuple is: (Button Label, PowerShell Command String)
# ---------------------------
base_commands = [
    ("Delete All Temps", '$userTemp = [System.IO.Path]::GetTempPath(); if (Test-Path $userTemp) { Write-Output "Purging user temp folder: $userTemp"; Get-ChildItem -Path $userTemp -Recurse -Force -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue; } else { Write-Output "User temp folder does not exist: $userTemp"; }'),
    ("Check For Updates", 'Install-Module -Name PSWindowsUpdate -Force; Import-Module PSWindowsUpdate; Get-WindowsUpdate; Install-WindowsUpdate -AcceptAll -Confirm:$false'),
    ("SFC /scannow", "sfc /scannow"),
    ("DISM /CheckHealth", "DISM /Online /Cleanup-Image /CheckHealth"),
    ("DISM /ScanHealth", "DISM /Online /Cleanup-Image /ScanHealth"),
    ("DISM /RestoreHealth", "DISM /Online /Cleanup-Image /RestoreHealth"),
    ("Analyze & Cleanup", "DISM /Online /Cleanup-Image /AnalyzeComponentStore; DISM /Online /Cleanup-Image /StartComponentCleanup"),
    ("Reset TCP/IP", "netsh int ip reset"),
    ("Reset/Renew IP", "ipconfig /release; ipconfig /renew"),
    ("Reset Winsock", "netsh winsock reset"),
    ("Flush DNS", "ipconfig /flushdns"),
    ("Clear All Logs", 'del /F /S /Q "C:\\*.log"'),
    ("Cleanmgr", "cleanmgr"),
    ("Clear Event Logs", "Get-WinEvent -ListLog * | ForEach-Object { Clear-WinEvent -LogName $_.LogName }"),
    ("Compact Windows", "compact.exe /CompactOS:always"),
    ("Update Drivers", "Install-Module -Name PSWindowsUpdate -Force; Import-Module PSWindowsUpdate; Get-WUDriver; Install-WUDriver -AcceptAll -Confirm:$false"),
    ("Optimize Disk", "Optimize-Volume -DriveLetter C"),
    ("Enable TCP Scaling", "netsh int tcp set global autotuninglevel=normal"),
    ("Reclaim Space", "DISM /Online /Cleanup-Image /StartComponentCleanup /ResetBase"),
    ("Optimize TCP", "netsh int tcp set global congestionprovider=ctcp"),
    ("Direct Cache", "netsh int tcp set global directcacheaccess=enabled")
]

additional_commands = [
    ("CHKDSK /f", "chkdsk C: /f"),
    ("Clear Update Cache", "Stop-Service wuauserv; Remove-Item -Recurse -Force C:\\Windows\\SoftwareDistribution\\Download; Start-Service wuauserv"),
    ("Disable Hibernation", "powercfg /hibernate off"),
    ("Clear Store Cache", "wsreset.exe"),
    ("Force Update", "UsoClient StartScan"),
    ("Restart Update Service", "Restart-Service wuauserv"),
    ("Reset Firewall", "netsh advfirewall reset"),
    ("Flush ARP", "netsh interface ip delete arpcache"),
    ("Cleanup Shadows", "vssadmin delete shadows /for=C: /all /quiet"),
    ("Disable Visual Effects", "Set-ItemProperty -Path 'HKCU:\\Control Panel\\Desktop\\WindowMetrics' -Name MinAnimate -Value 0"),
    ("Optimize Memory", "SystemPropertiesPerformance.exe"),
    ("Stop Spooler", "net stop spooler"),
    ("Restart Spooler", "net start spooler"),
    ("Disable WinSearch", "net stop wsearch; sc config WSearch start=disabled"),
    ("Enable WinSearch", "sc config WSearch start=delayed-auto; net start wsearch"),
    ("Clear Internet Cache", 'Remove-Item -Path "$env:LOCALAPPDATA\\Microsoft\\INetCache\\*" -Recurse -Force'),
    ("Show Sys Info", "systeminfo"),
    ("Repair Store", 'Get-AppXPackage -AllUsers | ForEach {Add-AppxPackage -DisableDevelopmentMode -Register "$($_.InstallLocation)\\AppXManifest.xml"}'),
    ("Clear Error Reports", 'del /F /S /Q "%LOCALAPPDATA%\\Microsoft\\Windows\\WER\\*"'),
    ("Clean Restore Points", "vssadmin delete shadows /all /quiet"),
    ("List Processes", "Get-Process"),
    ("Show IP Config", "ipconfig /all"),
    ("Clear Clipboard", "Clear-Clipboard"),
    ("List Net Adapters", "Get-NetAdapter"),
    ("Disable Sleep Timeout", "powercfg /change standby-timeout-ac 0"),
    ("Enable Sleep Timeout", "powercfg /change standby-timeout-ac 30"),
    ("Show Disk Usage", "Get-PSDrive -PSProvider FileSystem"),
    ("Defrag C:", "defrag C: -w"),
    ("Task Manager", "Start-Process taskmgr"),
    ("Services", "Start-Process services.msc"),
    ("List Programs", "Get-WmiObject -Class Win32_Product"),
    ("Clear Temp Files", "Remove-Item -Path $env:TEMP\\* -Recurse -Force"),
    ("Control Panel", "control"),
    ("Device Manager", "Start-Process devmgmt.msc"),
    ("Net Connections", "Start-Process ncpa.cpl"),
    ("Win Version", "winver"),
    ("Windows Update", "start ms-settings:windowsupdate"),
    ("Check Disk Health", "wmic diskdrive get status"),
    ("Update GP", "gpupdate /force"),
    ("Env Variables", "Get-ChildItem Env:"),
    ("Restart Explorer", "taskkill /f /im explorer.exe; start explorer.exe"),
    ("System Uptime", "(Get-Date) - (Get-CimInstance Win32_OperatingSystem).LastBootUpTime | Out-String"),
    ("List Scheduled Tasks", "Get-ScheduledTask"),
    ("List Services", "Get-Service"),
    ("Defender Status", "Get-MpComputerStatus"),
    ("Defender Quick Scan", "Start-MpScan -ScanType QuickScan"),
    ("Defender Full Scan", "Start-MpScan -ScanType FullScan"),
    ("List Hotfixes", "Get-HotFix"),
    ("Sys Log Errors", "Get-EventLog -LogName System -EntryType Error -Newest 20"),
    ("App Log Errors", "Get-EventLog -LogName Application -EntryType Error -Newest 20"),
    ("Startup Items", "Get-CimInstance -ClassName Win32_StartupCommand | Select-Object Name, Command"),
    ("Enable Firewall", "Set-NetFirewallProfile -All -Enabled True"),
    ("List USB Devices", "Get-PnpDevice -Class USB"),
    ("Disk Partitions", "Get-Partition"),
    ("Disk Volumes", "Get-Volume"),
    ("Disk Drives", "Get-Disk"),
    ("SMART Status", "Get-PhysicalDisk | Select-Object MediaType, OperationalStatus, HealthStatus"),
    ("CPU Usage", "Get-Counter '\\Processor(_Total)\\% Processor Time' -SampleInterval 1 -MaxSamples 5"),
    ("All Drivers", "driverquery"),
    ("Drivers Verbose", "driverquery /v /fo list"),
    ("BIOS Version", "Get-WmiObject Win32_BIOS | Select-Object Manufacturer, SMBIOSBIOSVersion"),
    ("Firewall Rules", "Get-NetFirewallRule"),
    ("Export SysInfo", "systeminfo > C:\\systeminfo.txt"),
    ("Defender History", "Get-MpThreatDetection"),
    ("Update Defender", "Update-MpSignature"),
    ("Backup Registry", 'reg export "HKLM\\Software" "C:\\backup_software.reg"'),
    ("Pending Reboots", 'if (Test-Path "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Component Based Servicing\\RebootPending") { Write-Output "Reboot pending" } else { Write-Output "No reboot pending" }'),
    ("Active Net Conns", "netstat -an"),
    ("ARP Table", "arp -a"),
    ("Sys Locale", "Get-Culture"),
    ("Sys Time", "Get-Date"),
    ("Memory Stats", "Get-Counter -Counter '\\Memory\\Available MBytes'"),
    ("Active TCP Conns", "netstat -at"),
    ("Listening Ports", "netstat -an | findstr LISTEN"),
    ("Disk Free", "Get-PSDrive -PSProvider FileSystem | Select-Object Name, Free, Used, @{Name='Total'; Expression={$_.Used + $_.Free}}"),
    ("List Apps (WMI)", "Get-WmiObject -Class Win32_Product"),
    ("Win Updates", "Get-HotFix"),
    ("Proc Details", "Get-Process | Format-Table -AutoSize"),
    ("Boot Time", "Get-CimInstance Win32_OperatingSystem | Select-Object LastBootUpTime"),
    ("Active IP Confs", "Get-NetIPConfiguration"),
    ("FW Profiles", "Get-NetFirewallProfile"),
    ("USB Controllers", "Get-PnpDevice -Class USBController"),
    ("Win License Info", "slmgr /dlv"),
    ("BitLocker Status", "manage-bde -status"),
    ("Proc by CPU", "Get-Process | Sort-Object CPU -Descending | Format-Table -AutoSize"),
    ("Boot Config", "bcdedit /enum"),
    ("TCP Conns", "netstat -at"),
    ("Listen TCP", 'netstat -an | findstr "LISTEN"'),
    ("Active IPs", "Get-NetIPAddress"),
    ("License Key", "wmic path SoftwareLicensingService get OA3xOriginalProductKey"),
    ("Sys Temp", "Get-WmiObject MSAcpi_ThermalZoneTemperature | Select-Object CurrentTemperature"),
    ("Fix Icons", "taskkill /f /im explorer.exe; start explorer.exe"),
    ("Enable SSH", """Add-WindowsCapability -Online -Name OpenSSH.Server;
Start-Service sshd;
Set-Service -Name sshd -StartupType 'Automatic';
New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22;
Get-Service sshd"""),
    ("Ram Usage", """$totalMemory = (Get-WmiObject Win32_ComputerSystem).TotalPhysicalMemory;
Get-Process | Sort-Object -Property WorkingSet -Descending | Select-Object Name, @{Name='MemoryUsage(MB)'; Expression={[math]::Round($_.WorkingSet / 1MB, 2)}}, @{Name='MemoryUsage(%)'; Expression={($_.WorkingSet / $totalMemory) * 100}}""")
]

# Combine all WinOptimize commands
all_commands = base_commands + additional_commands

# ---------------------------
# GUI Creation
# ---------------------------
def create_app(shortcuts_path):
    root = tk.Tk()
    root.title("Dark Shortcut & WinOptimize Launcher")
    root.configure(bg="black")
    root.geometry("1400x900")
    
    # --- Top Frame for Big Red "ALL" Button ---
    top_all_frame = tk.Frame(root, bg="black")
    top_all_frame.pack(fill=tk.X, pady=10)
    
    def run_all_everything():
        run_all_shortcuts()
        run_all_winopt()
    
    all_button = tk.Button(
        top_all_frame, text="ALL", command=run_all_everything,
        font=("Arial", 12, "bold"), bg="red", fg="white",
        activebackground="darkred", activeforeground="white",
        height=2, width=10
    )
    all_button.pack(padx=10, pady=10)
    
    # --- Create the Notebook ---
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)
    
    # ==============================
    # Tab 1: Shortcuts
    # ==============================
    shortcuts_tab = tk.Frame(notebook, bg="black")
    notebook.add(shortcuts_tab, text="Shortcuts")
    
    # Retrieve the full list of shortcuts
    shortcuts_list = find_all_shortcuts(shortcuts_path)
    
    # Top frame with Run All and Close All buttons
    top_frame_1 = tk.Frame(shortcuts_tab, bg="black")
    top_frame_1.pack(fill=tk.X, padx=10, pady=5)
    run_all_shortcuts_btn = tk.Button(
        top_frame_1, text="Run All", command=lambda: [launch_shortcut(path) for _, path in shortcuts_list],
        font=("Arial", 10, "bold"), bg="black", fg="white",
        activebackground="gray", activeforeground="white"
    )
    run_all_shortcuts_btn.pack(side=tk.LEFT, padx=5)
    close_all_btn = tk.Button(
        top_frame_1, text="Close All", command=close_all_apps,
        font=("Arial", 10, "bold"), bg="black", fg="white",
        activebackground="gray", activeforeground="white"
    )
    close_all_btn.pack(side=tk.RIGHT, padx=5)
    
    # Search Frame for Shortcuts
    search_frame_1 = tk.Frame(shortcuts_tab, bg="black")
    search_frame_1.pack(fill=tk.X, padx=10, pady=5)
    tk.Label(search_frame_1, text="Search Shortcuts:", font=("Arial", 10, "bold"), bg="black", fg="white").pack(side=tk.LEFT, padx=(0,5))
    search_entry_1 = tk.Entry(search_frame_1, font=("Arial", 10))
    search_entry_1.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    # Grid frame for shortcut buttons
    grid_frame = tk.Frame(shortcuts_tab, bg="black")
    grid_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    
    def populate_shortcuts_grid(filter_text=""):
        # Clear previous buttons
        for widget in grid_frame.winfo_children():
            widget.destroy()
        col_count = 5
        row = 0
        col = 0
        for name, path in shortcuts_list:
            if filter_text.lower() in name.lower():
                btn = tk.Button(
                    grid_frame, text=name,
                    command=lambda p=path: launch_shortcut(p),
                    font=("Arial", 10, "bold"), bg="black", fg="white",
                    activebackground="gray", activeforeground="white",
                    width=20, height=1
                )
                btn.grid(row=row, column=col, padx=5, pady=5)
                col += 1
                if col >= col_count:
                    col = 0
                    row += 1
    
    def on_search_shortcuts(event):
        query = search_entry_1.get()
        populate_shortcuts_grid(query)
    
    search_entry_1.bind("<KeyRelease>", on_search_shortcuts)
    
    # Initially populate with all shortcuts
    populate_shortcuts_grid()
    
    # ==============================
    # Tab 2: WinOptimize
    # ==============================
    winopt_tab = tk.Frame(notebook, bg="black")
    notebook.add(winopt_tab, text="WinOptimize")
    
    # Top frame with Run All for WinOptimize commands
    top_frame_2 = tk.Frame(winopt_tab, bg="black")
    top_frame_2.pack(fill=tk.X, padx=10, pady=5)
    def run_all_winopt():
        cmds = [cmd for (_, cmd) in all_commands]
        run_ps_all(cmds)
    run_all_winopt_btn = tk.Button(
        top_frame_2, text="Run All", command=run_all_winopt,
        font=("Arial", 10, "bold"), bg="black", fg="white",
        activebackground="gray", activeforeground="white"
    )
    run_all_winopt_btn.pack(padx=5, pady=5)
    
    # Search Frame for WinOptimize commands
    search_frame_2 = tk.Frame(winopt_tab, bg="black")
    search_frame_2.pack(fill=tk.X, padx=10, pady=5)
    tk.Label(search_frame_2, text="Search WinOptimize:", font=("Arial", 10, "bold"), bg="black", fg="white").pack(side=tk.LEFT, padx=(0,5))
    search_entry_2 = tk.Entry(search_frame_2, font=("Arial", 10))
    search_entry_2.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    # Grid frame for individual WinOptimize command buttons
    winopt_frame = tk.Frame(winopt_tab, bg="black")
    winopt_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    
    def populate_winopt_grid(filter_text=""):
        for widget in winopt_frame.winfo_children():
            widget.destroy()
        col_count = 5
        row = 0
        col = 0
        for label, cmd in all_commands:
            if filter_text.lower() in label.lower():
                btn = tk.Button(
                    winopt_frame, text=label,
                    command=lambda c=cmd: run_ps_individual(c),
                    font=("Arial", 10, "bold"), bg="black", fg="white",
                    activebackground="gray", activeforeground="white",
                    width=25, height=1
                )
                btn.grid(row=row, column=col, padx=5, pady=5)
                col += 1
                if col >= col_count:
                    col = 0
                    row += 1
    
    def on_search_winopt(event):
        query = search_entry_2.get()
        populate_winopt_grid(query)
    
    search_entry_2.bind("<KeyRelease>", on_search_winopt)
    
    # Initially populate with all commands
    populate_winopt_grid()
    
    root.mainloop()

if __name__ == "__main__":
    # Set your desired shortcuts folder path here
    shortcuts_directory = r"C:\Users\micha\Desktop\maintaince"
    create_app(shortcuts_directory)
