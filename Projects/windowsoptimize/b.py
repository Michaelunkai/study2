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
    no_option = "-N"
    wsl_shutdown = input("Do you want to shutdown WSL now? (yes/no): ")
    if wsl_shutdown.lower() == "yes":
        wsl_shutdown_command = "wsl --shutdown;"
    else:
        wsl_shutdown_command = ""
    
    command = (
        "choco upgrade all -y --force " + no_option + "; "
        "Repair-WindowsImage -Online -ScanHealth " + no_option + "; "
        "Repair-WindowsImage -Online -RestoreHealth " + no_option + "; "
        "sfc /scannow " + no_option + "; "
        "DISM.exe /Online /Cleanup-Image /CheckHealth " + no_option + "; "
        "DISM.exe /Online /Cleanup-Image /RestoreHealth " + no_option + "; "
        "dism /online /cleanup-image /startcomponentcleanup " + no_option + "; "
        "chkdsk /f /r " + no_option + "; "
        "net start wuauserv " + no_option + "; "
        "./updates.ps1 " + no_option + "; "
        "defrag C: /U /V " + no_option + "; "
        "netsh int ip reset " + no_option + "; "
        "netsh winsock reset " + no_option + "; "
        "dism /online /cleanup-image /analyzecomponentstore " + no_option + "; "
        "dism /online /cleanup-image /startcomponentcleanup " + no_option + "; "
        "ipconfig /flushdns " + no_option + "; "
        "Dism.exe /Online /Cleanup-Image /StartComponentCleanup " + no_option + "; "
        "Get-WindowsOptionalFeature -Online | Where-Object { $_.State -eq 'Enabled' } | Disable-WindowsOptionalFeature -Online " + no_option + "; "
        "wevtutil cl Application " + no_option + "; "
        "wevtutil cl Security " + no_option + "; "
        "wevtutil cl System " + no_option + "; "
        "Clear-DnsClientCache " + no_option + "; "
        "Get-AppXPackage -AllUsers | Foreach {Add-AppxPackage -DisableDevelopmentMode -Register \"$($_.InstallLocation)\\AppXManifest.xml\"} " + no_option + "; "
        "Start-MpScan -ScanType QuickScan " + no_option + "; "
        + wsl_shutdown_command +
        "wsl --unregister kali-linux; "
        "wsl --import kali-linux C:\\wsl2 C:\\backup\\linux\\wsl\\kalifull.tar; "
        "wsl --unregister ubuntu; "
        "wsl --import ubuntu C:\\wsl2\\ubuntu\\ C:\\backup\\linux\\wsl\\ubuntu.tar"
    )
    run_command_as_admin(command)
