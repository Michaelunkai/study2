import subprocess
import ctypes
import sys

def run_command_as_admin(command):
    try:
        if sys.platform.startswith('win'):
            # Check if the script is running as admin
            if ctypes.windll.shell32.IsUserAnAdmin() != 0:
                subprocess.run(["powershell", "-Command", command], shell=True, check=True)
            else:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", "powershell", "-Command " + command, None, 1)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    command = (
        "choco upgrade all -y --force; "
        "Repair-WindowsImage -Online -ScanHealth; "
        "Repair-WindowsImage -Online -RestoreHealth; "
        "sfc /scannow; "
        "DISM.exe /Online /Cleanup-Image /CheckHealth; "
        "DISM.exe /Online /Cleanup-Image /RestoreHealth; "
        "dism /online /cleanup-image /startcomponentcleanup; "
        "chkdsk /f /r; "
        "net start wuauserv; "
        "./updates.ps1; "
        "defrag C: /U /V; "
        "netsh int ip reset; "
        "netsh winsock reset; "
        "dism /online /cleanup-image /analyzecomponentstore; "
        "dism /online /cleanup-image /startcomponentcleanup; "
        "ipconfig /flushdns; "
        "Dism.exe /Online /Cleanup-Image /StartComponentCleanup; "
        "Get-WindowsOptionalFeature -Online | Where-Object { $_.State -eq 'Enabled' } | Disable-WindowsOptionalFeature -Online; "
        "wevtutil cl Application; "
        "wevtutil cl Security; "
        "wevtutil cl System; "
        "Clear-DnsClientCache; "
        "Get-AppXPackage -AllUsers | Foreach {Add-AppxPackage -DisableDevelopmentMode -Register \"$($_.InstallLocation)\\AppXManifest.xml\"}; "
        "Start-MpScan -ScanType QuickScan"
    )
    
    run_command_as_admin(command)
