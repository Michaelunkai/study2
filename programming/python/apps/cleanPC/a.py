import os
import subprocess
import tkinter as tk
from tkinter import ttk
import win32com.client  # pip install pywin32

# Global list to track processes launched via shortcuts
launched_processes = []

# Default font for bulky text on buttons
button_font = ("Arial", 10, "bold")

# ---------------------------
# Shortcuts Tab Functions
# ---------------------------
def find_unique_shortcuts(root_dir):
    """
    Recursively search for .lnk files under root_dir.
    For each folder, only the first encountered shortcut is kept.
    Returns a dictionary mapping folder name -> shortcut full path.
    """
    unique_shortcuts = {}
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(".lnk"):
                folder_name = os.path.basename(dirpath)
                if folder_name not in unique_shortcuts:
                    full_path = os.path.join(dirpath, filename)
                    unique_shortcuts[folder_name] = full_path
    return unique_shortcuts

def launch_shortcut(shortcut_path):
    """
    Launch the target of a Windows shortcut (.lnk) using WScript.Shell.
    Save the launched process so it can later be terminated.
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
    Terminate every process launched from the Shortcuts tab.
    """
    global launched_processes
    for proc in launched_processes:
        try:
            proc.terminate()
        except Exception as e:
            print(f"Error terminating process: {e}")
    launched_processes = []

# ---------------------------
# Helper: Run PowerShell in New Terminal
# ---------------------------
def run_powershell(ps_command):
    """
    Execute a PowerShell command in a new terminal window.
    Newlines are removed so the command is passed as a single line.
    """
    cmd_line = " ".join(ps_command.splitlines())
    try:
        subprocess.Popen(f'start powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "{cmd_line}"', shell=True)
    except Exception as e:
        print(f"Error running PowerShell command: {e}")

# ---------------------------
# WinOptimize Base Commands (Tab 2)
# ---------------------------
def delete_all_temps():
    ps_cmd = (
        '$userTemp = [System.IO.Path]::GetTempPath(); '
        'if (Test-Path $userTemp) { '
        'Write-Output "Purging user temp folder: $userTemp"; '
        'Get-ChildItem -Path $userTemp -Recurse -Force -ErrorAction SilentlyContinue | '
        'Remove-Item -Recurse -Force -ErrorAction SilentlyContinue; '
        '} else { '
        'Write-Output "User temp folder does not exist: $userTemp"; '
        '}'
    )
    run_powershell(ps_cmd)

def check_for_updates():
    ps_cmd = (
        'Install-Module -Name PSWindowsUpdate -Force; '
        'Import-Module PSWindowsUpdate; '
        'Get-WindowsUpdate; '
        'Install-WindowsUpdate -AcceptAll -Confirm:$false'
    )
    run_powershell(ps_cmd)

def run_sfc_scannow():
    run_powershell("sfc /scannow")

def run_dism_checkhealth():
    run_powershell("DISM /Online /Cleanup-Image /CheckHealth")

def run_dism_scanhealth():
    run_powershell("DISM /Online /Cleanup-Image /ScanHealth")

def run_dism_restorehealth():
    run_powershell("DISM /Online /Cleanup-Image /RestoreHealth")

def run_analyze_cleanup_component_store():
    run_powershell("DISM /Online /Cleanup-Image /AnalyzeComponentStore && DISM /Online /Cleanup-Image /StartComponentCleanup")

def reset_tcpip_stack():
    run_powershell("netsh int ip reset")

def reset_renew_ip():
    run_powershell("ipconfig /release && ipconfig /renew")

def reset_winsock():
    run_powershell("netsh winsock reset")

def flush_dns_cache():
    run_powershell("ipconfig /flushdns")

def clear_all_logs():
    run_powershell('del /F /S /Q "C:\\*.log"')

def run_cleanmgr():
    run_powershell("cleanmgr")

def clear_all_event_logs():
    run_powershell("Get-WinEvent -ListLog * | ForEach-Object { Clear-WinEvent -LogName $_.LogName }")

def compact_windows_installation():
    run_powershell("compact.exe /CompactOS:always")

def update_drivers():
    ps_cmd = (
        "Install-Module -Name PSWindowsUpdate -Force; "
        "Import-Module PSWindowsUpdate; "
        "Get-WUDriver; "
        "Install-WUDriver -AcceptAll -Confirm:$false"
    )
    run_powershell(ps_cmd)

def optimize_disk_caching():
    run_powershell("Optimize-Volume -DriveLetter C")

def enable_tcp_window_scaling():
    run_powershell("netsh int tcp set global autotuninglevel=normal")

def reclaim_unused_space():
    run_powershell("DISM /Online /Cleanup-Image /StartComponentCleanup /ResetBase")

def optimize_tcp_network_performance():
    run_powershell("netsh int tcp set global congestionprovider=ctcp")

def enable_direct_cache_access():
    run_powershell("netsh int tcp set global directcacheaccess=enabled")

# ---------------------------
# Additional Useful Commands (41 commands)
# ---------------------------
def run_chkdsk_f():
    run_powershell("chkdsk C: /f")

def clear_windows_update_cache():
    ps_cmd = (
        "Stop-Service wuauserv; "
        "Remove-Item -Recurse -Force C:\\Windows\\SoftwareDistribution\\Download; "
        "Start-Service wuauserv"
    )
    run_powershell(ps_cmd)

def disable_hibernation():
    run_powershell("powercfg /hibernate off")

def clear_windows_store_cache():
    run_powershell("wsreset.exe")

def force_windows_update_detection():
    run_powershell("UsoClient StartScan")

def restart_windows_update_service():
    run_powershell("Restart-Service wuauserv")

def reset_windows_firewall():
    run_powershell("netsh advfirewall reset")

def flush_arp_cache():
    run_powershell("netsh interface ip delete arpcache")

def cleanup_shadow_copies():
    run_powershell("vssadmin delete shadows /for=C: /all /quiet")

def disable_visual_effects():
    run_powershell("Set-ItemProperty -Path 'HKCU:\\Control Panel\\Desktop\\WindowMetrics' -Name MinAnimate -Value 0")

def optimize_virtual_memory():
    run_powershell("SystemPropertiesPerformance.exe")

def stop_print_spooler():
    run_powershell("net stop spooler")

def restart_print_spooler():
    run_powershell("net start spooler")

def disable_windows_search():
    run_powershell('net stop wsearch && sc config WSearch start=disabled')

def enable_windows_search():
    run_powershell('sc config WSearch start=delayed-auto && net start wsearch')

def clear_temp_internet_files():
    run_powershell('Remove-Item -Path "$env:LOCALAPPDATA\\Microsoft\\Windows\\INetCache\\*" -Recurse -Force')

def show_system_info():
    run_powershell("systeminfo")

def repair_windows_store():
    run_powershell('Get-AppXPackage -AllUsers | ForEach {Add-AppxPackage -DisableDevelopmentMode -Register "$($_.InstallLocation)\\AppXManifest.xml"}')

def clear_windows_error_reports():
    run_powershell(r'del /F /S /Q "%LOCALAPPDATA%\Microsoft\Windows\WER\*"')

def clean_system_restore_points():
    run_powershell("vssadmin delete shadows /all /quiet")

def list_running_processes():
    run_powershell("Get-Process")

def show_ip_configuration():
    run_powershell("ipconfig /all")

def clear_clipboard():
    run_powershell("Clear-Clipboard")

def list_network_adapters():
    run_powershell("Get-NetAdapter")

def disable_sleep_timeout():
    run_powershell("powercfg /change standby-timeout-ac 0")

def enable_sleep_timeout():
    run_powershell("powercfg /change standby-timeout-ac 30")

def show_disk_usage():
    run_powershell("Get-PSDrive -PSProvider FileSystem")

def defragment_c_drive():
    run_powershell("defrag C: -w")

def open_task_manager():
    run_powershell("Start-Process taskmgr")

def open_services():
    run_powershell("Start-Process services.msc")

def list_installed_programs():
    run_powershell("Get-WmiObject -Class Win32_Product")

def clear_temp_files():
    run_powershell("Remove-Item -Path $env:TEMP\\* -Recurse -Force")

def open_control_panel():
    run_powershell("control")

def open_device_manager():
    run_powershell("Start-Process devmgmt.msc")

def open_network_connections():
    run_powershell("Start-Process ncpa.cpl")

def show_windows_version():
    run_powershell("winver")

def open_windows_update_settings():
    run_powershell("start ms-settings:windowsupdate")

def check_disk_health():
    run_powershell("wmic diskdrive get status")

def update_group_policy():
    run_powershell("gpupdate /force")

def show_env_variables():
    run_powershell("Get-ChildItem Env:")

def restart_explorer():
    run_powershell("taskkill /f /im explorer.exe; start explorer.exe")

# ---------------------------
# Additional New Commands (50 new functions)
# ---------------------------
def show_system_uptime():
    run_powershell("(Get-Date) - (Get-CimInstance Win32_OperatingSystem).LastBootUpTime | Out-String")

def list_scheduled_tasks():
    run_powershell("Get-ScheduledTask")

def list_services():
    run_powershell("Get-Service")

def get_windows_defender_status():
    run_powershell("Get-MpComputerStatus")

def defender_quick_scan():
    run_powershell("Start-MpScan -ScanType QuickScan")

def defender_full_scan():
    run_powershell("Start-MpScan -ScanType FullScan")

def list_installed_hotfixes():
    run_powershell("Get-HotFix")

def check_system_event_log_errors():
    run_powershell("Get-EventLog -LogName System -EntryType Error -Newest 20")

def check_application_event_log_errors():
    run_powershell("Get-EventLog -LogName Application -EntryType Error -Newest 20")

def list_startup_items():
    run_powershell("Get-CimInstance -ClassName Win32_StartupCommand | Select-Object Name, Command")

def enable_windows_firewall():
    run_powershell("Set-NetFirewallProfile -All -Enabled True")

def list_usb_devices():
    run_powershell("Get-PnpDevice -Class USB")

def list_disk_partitions():
    run_powershell("Get-Partition")

def show_disk_volumes():
    run_powershell("Get-Volume")

def list_disk_drives():
    run_powershell("Get-Disk")

def check_smart_status():
    run_powershell("Get-PhysicalDisk | Select-Object MediaType, OperationalStatus, HealthStatus")

def monitor_cpu_usage():
    run_powershell("Get-Counter '\\Processor(_Total)\\% Processor Time' -SampleInterval 1 -MaxSamples 5")

def list_all_drivers():
    run_powershell("driverquery")

def list_all_drivers_verbose():
    run_powershell("driverquery /v /fo list")

def show_bios_version():
    run_powershell("Get-WmiObject Win32_BIOS | Select-Object Manufacturer, SMBIOSBIOSVersion")

def list_firewall_rules():
    run_powershell("Get-NetFirewallRule")

def export_system_info():
    run_powershell("systeminfo > C:\\systeminfo.txt")

def defender_scan_history():
    run_powershell("Get-MpThreatDetection")

def update_defender_definitions():
    run_powershell("Update-MpSignature")

def backup_registry():
    run_powershell('reg export "HKLM\\Software" "C:\\backup_software.reg"')

def check_pending_reboots():
    run_powershell('if (Test-Path "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Component Based Servicing\\RebootPending") { Write-Output "Reboot pending" } else { Write-Output "No reboot pending" }')

def list_active_network_connections():
    run_powershell("netstat -an")

def show_arp_table():
    run_powershell("arp -a")

def display_system_locale():
    run_powershell("Get-Culture")

def display_system_time():
    run_powershell("Get-Date")

def show_memory_statistics():
    run_powershell("Get-Counter -Counter '\\Memory\\Available MBytes'")

def list_active_tcp_connections():
    run_powershell("netstat -at")

def list_listening_ports():
    run_powershell("netstat -an | findstr LISTEN")

def show_disk_free_space():
    run_powershell("Get-PSDrive -PSProvider FileSystem | Select-Object Name, Free, Used, @{Name='Total'; Expression={$_.Used + $_.Free}}")

def list_installed_applications_wmi():
    run_powershell("Get-WmiObject -Class Win32_Product")

def list_windows_updates():
    run_powershell("Get-HotFix")

def list_running_processes_detailed():
    run_powershell("Get-Process | Format-Table -AutoSize")

def show_system_boot_time():
    run_powershell("Get-CimInstance Win32_OperatingSystem | Select-Object LastBootUpTime")

def show_active_network_interfaces():
    run_powershell("Get-NetIPConfiguration")

def list_firewall_profiles():
    run_powershell("Get-NetFirewallProfile")

def list_usb_controllers():
    run_powershell("Get-PnpDevice -Class USBController")

def show_windows_license_info():
    run_powershell("slmgr /dlv")

def check_bitlocker_status():
    run_powershell("manage-bde -status")

def list_processes_by_cpu():
    run_powershell("Get-Process | Sort-Object CPU -Descending | Format-Table -AutoSize")

def show_boot_configuration():
    run_powershell("bcdedit /enum")

def list_network_connections_tcp():
    run_powershell("netstat -at")

def list_listening_ports_tcp():
    run_powershell('netstat -an | findstr "LISTEN"')

def list_active_ip_addresses():
    run_powershell("Get-NetIPAddress")

def show_windows_license_key_info():
    run_powershell("wmic path SoftwareLicensingService get OA3xOriginalProductKey")

def display_system_temperature():
    run_powershell("Get-WmiObject MSAcpi_ThermalZoneTemperature | Select-Object CurrentTemperature")

# ---------------------------
# New: Fix Icons Command (Restart Explorer)
# ---------------------------
def fix_icons():
    run_powershell("taskkill /f /im explorer.exe; start explorer.exe")

# ---------------------------
# New: Enable SSH Command
# ---------------------------
def enable_ssh():
    ps_script = r"""
Add-WindowsCapability -Online -Name OpenSSH.Server;
Start-Service sshd;
Set-Service -Name sshd -StartupType 'Automatic';
New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22;
Get-Service sshd
"""
    run_powershell(ps_script)

# ---------------------------
# New: Ram Usage Command
# ---------------------------
def ram_usage():
    ps_script = r"""
$totalMemory = (Get-WmiObject Win32_ComputerSystem).TotalPhysicalMemory;
Get-Process | Sort-Object -Property WorkingSet -Descending | Select-Object Name, @{Name='MemoryUsage(MB)'; Expression={[math]::Round($_.WorkingSet / 1MB, 2)}}, @{Name='MemoryUsage(%)'; Expression={($_.WorkingSet / $totalMemory) * 100}}
"""
    run_powershell(ps_script)

# ---------------------------
# GUI Creation
# ---------------------------
def create_app(root_dir):
    root = tk.Tk()
    root.title("Dark Shortcut & WinOptimize Launcher")
    root.configure(bg="black")
    root.geometry("1400x900")
    
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)
    
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TNotebook", background="black")
    style.configure("TNotebook.Tab", background="black", foreground="white")
    
    # ----- Tab 1: Shortcuts -----
    shortcuts_tab = tk.Frame(notebook, bg="black")
    notebook.add(shortcuts_tab, text="Shortcuts")
    
    unique_shortcuts = find_unique_shortcuts(root_dir)
    def run_all_shortcuts():
        for path in unique_shortcuts.values():
            launch_shortcut(path)
    
    top_frame_1 = tk.Frame(shortcuts_tab, bg="black")
    top_frame_1.pack(fill=tk.X)
    run_all_shortcuts_btn = tk.Button(top_frame_1, text="Run All", command=run_all_shortcuts,
                                      font=button_font, bg="black", fg="white", activebackground="gray", activeforeground="white")
    run_all_shortcuts_btn.pack(side=tk.LEFT, padx=10, pady=10)
    close_all_btn = tk.Button(top_frame_1, text="Close All", command=close_all_apps,
                              font=button_font, bg="black", fg="white", activebackground="gray", activeforeground="white")
    close_all_btn.pack(side=tk.RIGHT, padx=10, pady=10)
    
    grid_frame = tk.Frame(shortcuts_tab, bg="black")
    grid_frame.pack(padx=10, pady=10)
    for i, folder_name in enumerate(unique_shortcuts.keys()):
        row = i // 10
        col = i % 10
        btn = tk.Button(grid_frame, text=folder_name,
                        command=lambda sp=unique_shortcuts[folder_name]: launch_shortcut(sp),
                        font=button_font, bg="black", fg="white", activebackground="gray", activeforeground="white",
                        width=10, height=1)
        btn.grid(row=row, column=col, padx=5, pady=5)
    
    # ----- Tab 2: WinOptimize -----
    winopt_tab = tk.Frame(notebook, bg="black")
    notebook.add(winopt_tab, text="WinOptimize")
    
    winopt_buttons = [
        ("Delete All Temps", delete_all_temps),
        ("Check For Updates", check_for_updates),
        ("SFC /scannow", run_sfc_scannow),
        ("DISM /CheckHealth", run_dism_checkhealth),
        ("DISM /ScanHealth", run_dism_scanhealth),
        ("DISM /RestoreHealth", run_dism_restorehealth),
        ("Analyze & Cleanup", run_analyze_cleanup_component_store),
        ("Reset TCP/IP", reset_tcpip_stack),
        ("Reset/Renew IP", reset_renew_ip),
        ("Reset Winsock", reset_winsock),
        ("Flush DNS", flush_dns_cache),
        ("Clear All Logs", clear_all_logs),
        ("Cleanmgr", run_cleanmgr),
        ("Clear Event Logs", clear_all_event_logs),
        ("Compact Windows", compact_windows_installation),
        ("Update Drivers", update_drivers),
        ("Optimize Disk", optimize_disk_caching),
        ("Enable TCP Scaling", enable_tcp_window_scaling),
        ("Reclaim Space", reclaim_unused_space),
        ("Optimize TCP", optimize_tcp_network_performance),
        ("Direct Cache", enable_direct_cache_access)
    ]
    
    additional_commands = [
        ("CHKDSK /f", run_chkdsk_f),
        ("Clear Update Cache", clear_windows_update_cache),
        ("Disable Hibernation", disable_hibernation),
        ("Clear Store Cache", clear_windows_store_cache),
        ("Force Update", force_windows_update_detection),
        ("Restart Update Service", restart_windows_update_service),
        ("Reset Firewall", reset_windows_firewall),
        ("Flush ARP", flush_arp_cache),
        ("Cleanup Shadows", cleanup_shadow_copies),
        ("Disable Visual Effects", disable_visual_effects),
        ("Optimize Memory", optimize_virtual_memory),
        ("Stop Spooler", stop_print_spooler),
        ("Restart Spooler", restart_print_spooler),
        ("Disable WinSearch", disable_windows_search),
        ("Enable WinSearch", enable_windows_search),
        ("Clear Internet Cache", clear_temp_internet_files),
        ("Show Sys Info", show_system_info),
        ("Repair Store", repair_windows_store),
        ("Clear Error Reports", clear_windows_error_reports),
        ("Clean Restore Points", clean_system_restore_points),
        ("List Processes", list_running_processes),
        ("Show IP Config", show_ip_configuration),
        ("Clear Clipboard", clear_clipboard),
        ("List Net Adapters", list_network_adapters),
        ("Disable Sleep Timeout", disable_sleep_timeout),
        ("Enable Sleep Timeout", enable_sleep_timeout),
        ("Show Disk Usage", show_disk_usage),
        ("Defrag C:", defragment_c_drive),
        ("Task Manager", open_task_manager),
        ("Services", open_services),
        ("List Programs", list_installed_programs),
        ("Clear Temp Files", clear_temp_files),
        ("Control Panel", open_control_panel),
        ("Device Manager", open_device_manager),
        ("Net Connections", open_network_connections),
        ("Win Version", show_windows_version),
        ("Windows Update", open_windows_update_settings),
        ("Check Disk Health", check_disk_health),
        ("Update GP", update_group_policy),
        ("Env Variables", show_env_variables),
        ("Restart Explorer", restart_explorer),
        ("System Uptime", show_system_uptime),
        ("List Scheduled Tasks", list_scheduled_tasks),
        ("List Services", list_services),
        ("Defender Status", get_windows_defender_status),
        ("Defender Quick Scan", defender_quick_scan),
        ("Defender Full Scan", defender_full_scan),
        ("List Hotfixes", list_installed_hotfixes),
        ("Sys Log Errors", check_system_event_log_errors),
        ("App Log Errors", check_application_event_log_errors),
        ("Startup Items", list_startup_items),
        ("Enable Firewall", enable_windows_firewall),
        ("List USB Devices", list_usb_devices),
        ("Disk Partitions", list_disk_partitions),
        ("Disk Volumes", show_disk_volumes),
        ("Disk Drives", list_disk_drives),
        ("SMART Status", check_smart_status),
        ("CPU Usage", monitor_cpu_usage),
        ("All Drivers", list_all_drivers),
        ("Drivers Verbose", list_all_drivers_verbose),
        ("BIOS Version", show_bios_version),
        ("Firewall Rules", list_firewall_rules),
        ("Export SysInfo", export_system_info),
        ("Defender History", defender_scan_history),
        ("Update Defender", update_defender_definitions),
        ("Backup Registry", backup_registry),
        ("Pending Reboots", check_pending_reboots),
        ("Active Net Conns", list_active_network_connections),
        ("ARP Table", show_arp_table),
        ("Sys Locale", display_system_locale),
        ("Sys Time", display_system_time),
        ("Memory Stats", show_memory_statistics),
        ("Active TCP Conns", list_active_tcp_connections),
        ("Listening Ports", list_listening_ports),
        ("Disk Free", show_disk_free_space),
        ("List Apps (WMI)", list_installed_applications_wmi),
        ("Win Updates", list_windows_updates),
        ("Proc Details", list_running_processes_detailed),
        ("Boot Time", show_system_boot_time),
        ("Active IP Confs", show_active_network_interfaces),
        ("FW Profiles", list_firewall_profiles),
        ("USB Controllers", list_usb_controllers),
        ("Win License Info", show_windows_license_info),
        ("BitLocker Status", check_bitlocker_status),
        ("Proc by CPU", list_processes_by_cpu),
        ("Boot Config", show_boot_configuration),
        ("TCP Conns", list_network_connections_tcp),
        ("Listen TCP", list_listening_ports_tcp),
        ("Active IPs", list_active_ip_addresses),
        ("License Key", show_windows_license_key_info),
        ("Sys Temp", display_system_temperature),
        ("Fix Icons", fix_icons)
    ]
    all_winopt_commands = winopt_buttons + additional_commands
    
    def run_all_winopt_commands():
        for label, command in all_winopt_commands:
            command()
    
    top_frame_2 = tk.Frame(winopt_tab, bg="black")
    top_frame_2.pack(fill=tk.X)
    run_all_winopt_btn = tk.Button(top_frame_2, text="Run All", command=run_all_winopt_commands,
                                   font=button_font, bg="black", fg="white", activebackground="gray", activeforeground="white")
    run_all_winopt_btn.pack(padx=10, pady=10)
    
    winopt_frame = tk.Frame(winopt_tab, bg="black")
    winopt_frame.pack(padx=10, pady=10)
    for i, (label, command) in enumerate(all_winopt_commands):
        row = i // 10
        col = i % 10
        btn = tk.Button(winopt_frame, text=label, command=command,
                        font=button_font, bg="black", fg="white", activebackground="gray", activeforeground="white",
                        width=15, height=1)
        btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    
    root.mainloop()

if __name__ == "__main__":
    backup_path = r"C:\backup\windowsapps\installed"
    create_app(backup_path)
