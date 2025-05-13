import subprocess
import time
import psutil
import os
import shutil
from collections import defaultdict
import difflib

# Define important processes (all names in lowercase)
IMPORTANT_PROCESSES = {
    "system idle process", "system", "csrss.exe", "wininit.exe", "winlogon.exe",
    "services.exe", "lsass.exe", "smss.exe", "svchost.exe", "explorer.exe"
}

# ANSI escape codes for colors and formatting
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
RESET = "\033[0m"

def set_process_priority(pid, priority):
    """
    Sets the priority of a process given its PID.
    Available priorities:
        psutil.IDLE_PRIORITY_CLASS  -> Minimize resource usage
        psutil.NORMAL_PRIORITY_CLASS -> Default
        psutil.HIGH_PRIORITY_CLASS  -> Maximize resource usage
    """
    try:
        proc = psutil.Process(pid)
        proc.nice(priority)
        print(f"{GREEN}{BOLD}Set process {pid} priority to {priority}{RESET}")
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        print(f"{RED}{BOLD}Failed to change priority for PID {pid}{RESET}")

def get_windows_processes():
    """
    Retrieves a list of processes with aggregated CPU and memory usage.
    Returns a list of tuples: (Process Name, Instance Count, Total CPU %, Total Memory (MB), [PIDs])
    """
    process_dict = defaultdict(lambda: {"count": 0, "cpu": 0.0, "memory": 0.0, "pids": []})

    try:
        time.sleep(0.5)  # Brief pause for better CPU readings
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                name = proc.info['name']
                pid = proc.info['pid']
                cpu_percent = proc.info['cpu_percent']
                mem_mb = proc.info['memory_info'].rss / (1024 * 1024)

                process_dict[name]["count"] += 1
                process_dict[name]["cpu"] += cpu_percent
                process_dict[name]["memory"] += mem_mb
                process_dict[name]["pids"].append(pid)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
    except Exception as e:
        print(f"{RED}{BOLD}Error retrieving processes: {e}{RESET}")

    processes = [(name, data["count"], data["cpu"], data["memory"], data["pids"]) for name, data in process_dict.items()]
    return sorted(processes, key=lambda x: x[3])  # Sort by memory usage in ascending order

def display_processes(processes):
    """Displays the process list in a formatted table."""
    header = f"{BOLD}{UNDERLINE}{WHITE}{'No.':<4} {'Process Name':<30} {'Instances':<10} {'CPU (%)':<10} {'Memory (MB)':<12}{RESET}"
    print(header)
    for idx, (name, count, cpu, mem, pids) in enumerate(processes, start=1):
        color = RED if name.lower() in IMPORTANT_PROCESSES else RESET
        print(f"{idx:<4} {color}{name:<30}{RESET} {count:<10} {cpu:.2f}{mem:>12.2f}")

def main():
    """Main loop for interacting with the user."""
    while True:
        print("\n" + "=" * 80)
        processes = get_windows_processes()
        display_processes(processes)

        user_command = input(f"\n{BOLD}Enter process number to modify (or 'exit' to quit): {RESET}").strip().lower()
        if user_command == "exit":
            break
        
        try:
            idx = int(user_command) - 1
            if idx < 0 or idx >= len(processes):
                print(f"{RED}{BOLD}Invalid process number.{RESET}")
                continue
            
            process_name, _, _, _, pids = processes[idx]
            action = input(f"{BOLD}Enter 'minimize' to reduce resource usage or 'maximize' to prioritize: {RESET}").strip().lower()
            
            if action == "minimize":
                for pid in pids:
                    set_process_priority(pid, psutil.IDLE_PRIORITY_CLASS)
            elif action == "maximize":
                for pid in pids:
                    set_process_priority(pid, psutil.HIGH_PRIORITY_CLASS)
            else:
                print(f"{YELLOW}{BOLD}Invalid action.{RESET}")
        except ValueError:
            print(f"{RED}{BOLD}Invalid input.{RESET}")
        time.sleep(1)

if __name__ == "__main__":
    main()
