import curses
import subprocess
import ctypes
import sys
import os

# Define the commands
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
    {"name": "Start Defender Scan", "command": "Start-MpScan -ScanType QuickScan"},
    {"name": "Defender full Scan", "command": "Start-MpScan -ScanType FullScan"},
    {"name": "Unregister Kali WSL", "command": "wsl --unregister kali-linux"},
    {"name": "Import Kali WSL", "command": "wsl --import kali-linux C:\\wsl2 C:\\backup\\linux\\wsl\\kalifull.tar"},
    {"name": "Unregister Ubuntu WSL", "command": "wsl --unregister ubuntu"},
    {"name": "Import Ubuntu WSL", "command": "wsl --import ubuntu C:\\wsl2\\ubuntu\\ C:\\backup\\linux\\wsl\\ubuntu.tar"},
    {"name": "Export WSL2 distros", "command": "wsl --export kali-linux C:\\backup\\linux\\kalifull.tar; wsl --export ubuntu C:\\backup\\linux\\ubuntu.tar"},
    {"name": "Turbo Mod", "command": "python C:\\backup\\windowsapps\\powerplans\\turbo.py"},
    {"name": "PowerSaving Mod", "command": "python C:\\backup\\windowsapps\\powerplans\\powersavings.py"},
    {"name": "Disable Windows Firewall", "command": "Set-MpPreference -DisableRealtimeMonitoring $true; Set-NetFirewallProfile -Profile Domain, Private, Public -Enabled False"},
    {"name": "Enable Windows Firewall", "command": "Set-MpPreference -DisableRealtimeMonitoring $false; Set-NetFirewallProfile -Profile Domain, Private, Public -Enabled True"},
    {"name": "Enable SSH", "command": "Add-WindowsCapability -Online -Name OpenSSH.Server; Start-Service sshd; Set-Service -Name sshd -StartupType 'Automatic'; New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22; Get-Service sshd"},
    {"name": "Ram Usage", "command": "$totalMemory = (Get-WmiObject Win32_ComputerSystem).TotalPhysicalMemory; Get-Process | Sort-Object -Property WorkingSet -Descending | Select-Object Name, @{Name='MemoryUsage(MB)'; Expression={[math]::Round($_.WorkingSet / 1MB, 2)}}, @{Name='MemoryUsage(%)'; Expression={($_.WorkingSet / $totalMemory) * 100}}"},
    {"name": "cleanmgr Tool", "command": "cleanmgr /sageset:1"},
]

bulk_commands = ["Update choco Packages", "Scan System Health", "Restore System Health", "Check System Files", "Check Image Health", "Restore Image Health", "Cleanup Component Store", "Start Update Service", "windows updates", "Defragment C Drive", "Reset TCP/IP Stack", "Reset Winsock", "Analyze Component Store", "Cleanup Component Store", "Flush DNS Cache", "Clear Application Log", "Clear Security Log", "Clear System Log", "Clear DNS Cache", "Start Defender Scan", "Reset/Renew IP", "cleanmgr Tool"]
wsl2_commands = ["Unregister Kali WSL", "Import Kali WSL", "Unregister Ubuntu WSL", "Import Ubuntu WSL"]

# Run command as admin
def run_command_as_admin(command):
    try:
        if sys.platform.startswith('win'):
            if ctypes.windll.shell32.IsUserAnAdmin() != 0:
                subprocess.Popen(["powershell", "-NoExit", "-Command", command], shell=True)
            else:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", "powershell", "-NoExit -Command " + command, None, 1)
    except Exception as e:
        print("Error:", e)

def run_selected_commands(selected_commands):
    commands_script = "\n".join(selected_commands)
    script_file = os.path.join(os.path.expanduser("~"), "commands_script.ps1")
    
    with open(script_file, "w") as file:
        file.write(commands_script)
    
    run_command_as_admin(f"& '{script_file}'")

# Main loop using curses
def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    current_tab = 0
    current_selection = 0
    command_selection = [False] * len(commands)
    
    def draw_menu():
        stdscr.clear()
        tabs = ["Not Bulk", "Bulk", "WSL2"]
        y, x = stdscr.getmaxyx()
        
        for i, tab in enumerate(tabs):
            if i == current_tab:
                stdscr.addstr(0, i*10, tab, curses.A_REVERSE)
            else:
                stdscr.addstr(0, i*10, tab)
        
        current_commands = get_current_tab_commands(current_tab)
        max_items_to_display = y - 5
        
        for i, cmd in enumerate(current_commands):
            if i >= max_items_to_display:
                break
            display_str = "[X] " + cmd["name"] if command_selection[commands.index(cmd)] else "[ ] " + cmd["name"]
            if i == current_selection:
                stdscr.addstr(i+2, 2, display_str, curses.A_REVERSE)
            else:
                stdscr.addstr(i+2, 2, display_str)

        stdscr.addstr(y-3, 2, "Press Z to select all, X to deselect all")
        stdscr.addstr(y-2, 2, "Press TAB to switch tabs")
        stdscr.addstr(y-1, 2, "Press SPACE to select/deselect commands, ENTER to run selected commands")
        stdscr.refresh()

    def get_current_tab_commands(tab_index):
        if tab_index == 0:
            return [cmd for cmd in commands if cmd["name"] not in bulk_commands + wsl2_commands]
        elif tab_index == 1:
            return [cmd for cmd in commands if cmd["name"] in bulk_commands]
        else:
            return [cmd for cmd in commands if cmd["name"] in wsl2_commands]

    def select_all():
        current_commands = get_current_tab_commands(current_tab)
        for cmd in current_commands:
            command_selection[commands.index(cmd)] = True

    def deselect_all():
        current_commands = get_current_tab_commands(current_tab)
        for cmd in current_commands:
            command_selection[commands.index(cmd)] = False

    while True:
        draw_menu()
        key = stdscr.getch()
        
        if key == 9:  # TAB key
            current_tab = (current_tab + 1) % 3
            current_selection = 0
        elif key == 10:  # ENTER key
            selected_cmds = [cmd["command"] for i, cmd in enumerate(commands) if command_selection[i]]
            run_selected_commands(selected_cmds)
        elif key == 32:  # SPACE key
            current_commands = get_current_tab_commands(current_tab)
            command_selection[commands.index(current_commands[current_selection])] = not command_selection[commands.index(current_commands[current_selection])]
        elif key == curses.KEY_UP:
            current_selection = max(current_selection - 1, 0)
        elif key == curses.KEY_DOWN:
            current_commands = get_current_tab_commands(current_tab)
            current_selection = min(current_selection + 1, len(current_commands) - 1)
        elif key == ord('z'):
            select_all()
        elif key == ord('x'):
            deselect_all()

if __name__ == "__main__":
    curses.wrapper(main)
    
