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

def get_windows_processes():
    """
    Retrieves a list of processes with aggregated CPU and memory usage.
    Returns a list of tuples: (Process Name, Instance Count, Total CPU %, Total Memory (MB), [PIDs])
    """
    process_dict = defaultdict(lambda: {"count": 0, "cpu": 0.0, "memory": 0.0, "pids": []})
    try:
        # Prime CPU measurements (this pass initializes CPU percent values)
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            pass
        time.sleep(0.5)  # Brief pause for better CPU readings
        # Aggregate data from each process
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
    processes = []
    for name, data in process_dict.items():
        processes.append((name, data["count"], data["cpu"], data["memory"], data["pids"]))
    return processes

def display_processes(processes):
    """
    Sorts and displays the process list along with an index number.
    Processes are sorted in ascending order by memory usage.
    Processes matching important system names are highlighted in red.
    Returns the sorted list.
    """
    processes_sorted = sorted(processes, key=lambda x: x[3])
    try:
        terminal_width = shutil.get_terminal_size().columns
    except Exception:
        terminal_width = 100
    header = f"{BOLD}{UNDERLINE}{WHITE}{'No.':<4} {'Process Name':<30} {'Instances':<10} {'CPU (%)':<10} {'Memory (MB)':<12}{RESET}"
    print(header)
    for idx, (name, count, cpu, mem, pids) in enumerate(processes_sorted, start=1):
        idx_str = f"{idx:<4}"
        name_str = f"{name:<30}"
        count_str = f"{count:<10}"
        cpu_str = f"{cpu:.2f}".rjust(10)
        mem_str = f"{mem:.2f}".rjust(12)
        color = RED if name.lower() in IMPORTANT_PROCESSES else RESET
        print(f"{idx_str} {color}{name_str}{RESET} {count_str} {cpu_str} {mem_str}")
    print("-" * terminal_width)
    total_instances = sum(count for _, count, _, _, _ in processes_sorted)
    total_memory = sum(mem for _, _, _, mem, _ in processes_sorted)
    print(f"{BOLD}Total: {len(processes_sorted)} unique processes, {total_instances} instances, {total_memory:.2f} MB used{RESET}")
    return processes_sorted

def display_system_overview():
    """
    Displays overall system CPU and memory usage.
    """
    overall_cpu = psutil.cpu_percent(interval=0.1)
    overall_mem = psutil.virtual_memory().percent
    overview_text = f"Overall CPU Usage: {overall_cpu:.1f}%   Overall Memory Usage: {overall_mem:.1f}%"
    print(f"{BOLD}{CYAN}{overview_text}{RESET}")

def search_processes(processes, search_term):
    """
    Filters the process list based on a search term using fuzzy matching.
    In addition to the process name, it also checks the process command line.
    Returns the filtered list.
    """
    filtered = []
    search_lower = search_term.lower()
    for proc in processes:
        name, count, cpu, mem, pids = proc
        # Check the process name first
        name_match = search_lower in name.lower() or difflib.SequenceMatcher(None, search_lower, name.lower()).ratio() > 0.6
        cmdline_match = False
        # Attempt to check the command line of the first PID
        try:
            proc_obj = psutil.Process(pids[0])
            cmdline = " ".join(proc_obj.cmdline()).lower()
            cmdline_match = search_lower in cmdline or difflib.SequenceMatcher(None, search_lower, cmdline).ratio() > 0.6
        except Exception:
            cmdline_match = False
        if name_match or cmdline_match:
            filtered.append(proc)
    return filtered

def kill_processes_by_image(processes):
    """
    Prompts the user to select processes (by index) and kills them using taskkill.exe.
    """
    user_input = input(f"\n{BOLD}Enter process numbers to kill (e.g. 1,3,5) or press Enter to cancel: {RESET}").strip()
    if not user_input:
        print(f"{YELLOW}{BOLD}No processes selected for killing. Returning to main menu.{RESET}")
        return
    parts = user_input.replace(",", " ").split()
    indices = []
    for part in parts:
        try:
            idx = int(part) - 1
            if idx < 0 or idx >= len(processes):
                print(f"{RED}{BOLD}Index {part} out of range.{RESET}")
                return
            indices.append(idx)
        except ValueError:
            print(f"{RED}{BOLD}Invalid number: {part}.{RESET}")
            return
    pids_dict = {}
    for idx in indices:
        proc = processes[idx]
        name = proc[0]
        if name in pids_dict:
            pids_dict[name].extend(proc[4])
        else:
            pids_dict[name] = proc[4].copy()
    for name in pids_dict.keys():
        try:
            result = subprocess.run(
                ['taskkill.exe', '/F', '/IM', name],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"{GREEN}{BOLD}Killed all processes with image name '{name}'.{RESET}")
            print(result.stdout.strip())
        except subprocess.CalledProcessError as e:
            print(f"{RED}{BOLD}Error killing processes with image name '{name}':{RESET}")
            print(e.stderr.strip())

def main():
    """
    Main loop: displays process list, system overview, and search option.
    """
    while True:
        print("\n" + "=" * 80)
        print(f"{BOLD}{CYAN}Process Monitor{RESET}")
        processes = get_windows_processes()
        processes_sorted = display_processes(processes)
        display_system_overview()
        print(f"\n{BOLD}{CYAN}Options:\n[S] Search processes\n[E] Exit{RESET}")
        command = input(f"{BOLD}Enter option: {RESET}").strip().lower()
        if command == "e":
            print(f"{GREEN}{BOLD}Exiting...{RESET}")
            break
        elif command == "s":
            search_term = input(f"{BOLD}Enter search term: {RESET}").strip()
            if not search_term:
                print(f"{YELLOW}{BOLD}No search term entered. Returning to main menu.{RESET}")
                continue
            filtered_processes = search_processes(processes_sorted, search_term)
            if not filtered_processes:
                print(f"{YELLOW}{BOLD}No processes matching '{search_term}' found.{RESET}")
                continue
            print(f"\n{CYAN}{BOLD}Search results for '{search_term}':{RESET}")
            filtered_sorted = display_processes(filtered_processes)
            kill_processes_by_image(filtered_sorted)
        else:
            print(f"{YELLOW}{BOLD}Unknown command. Please try again.{RESET}")
        time.sleep(1)

if __name__ == "__main__":
    main()