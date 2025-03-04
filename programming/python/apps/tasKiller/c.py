import subprocess
import time
import psutil
import difflib

# ANSI escape codes for colors and formatting
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
WHITE = "\033[97m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Track suspended processes
suspended_processes = {}

def get_windows_processes():
    """
    Retrieves a list of processes with aggregated CPU and memory usage.
    Returns a list of tuples: (Process Name, Instance Count, Total CPU %, Total Memory (MB), [PIDs])
    """
    process_dict = {}

    try:
        # Prime CPU measurements (this pass initializes CPU percent values)
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            pass

        time.sleep(0.5)  # Brief pause for better CPU readings

        # Now aggregate data
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                name = proc.info['name']
                pid = proc.info['pid']
                cpu_percent = proc.info['cpu_percent']
                mem_mb = proc.info['memory_info'].rss / (1024 * 1024)

                if name not in process_dict:
                    process_dict[name] = {"count": 0, "cpu": 0.0, "memory": 0.0, "pids": []}

                process_dict[name]["count"] += 1
                process_dict[name]["cpu"] += cpu_percent
                process_dict[name]["memory"] += mem_mb
                process_dict[name]["pids"].append(pid)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
    except Exception as e:
        print(f"{RED}{BOLD}Error retrieving processes: {e}{RESET}")

    # Convert dictionary to list of tuples
    processes = [(name, data["count"], data["cpu"], data["memory"], data["pids"]) for name, data in process_dict.items()]
    return processes

def display_processes(processes):
    """
    Displays the process list sorted from least to most resource usage (CPU + memory).
    """
    # Sort by total resource usage (CPU + memory)
    processes_sorted = sorted(processes, key=lambda x: x[2] + x[3])

    print(f"\n{BOLD}{WHITE}{'Process Name':<30} {'Instances':<10} {'CPU (%)':<10} {'Memory (MB)':<12}{RESET}")
    for name, count, cpu, mem, pids in processes_sorted:
        print(f"{name:<30} {count:<10} {cpu:.2f}".rjust(10) + f" {mem:.2f}".rjust(12))

    print(f"\n{BOLD}Total processes: {len(processes_sorted)}{RESET}")
    return processes_sorted

def find_matching_processes(processes, search_term):
    """
    Finds processes that match the search term using fuzzy matching.
    Returns a list of matching process names.
    """
    matches = []
    search_lower = search_term.lower()
    for name, _, _, _, _ in processes:
        name_lower = name.lower()
        if search_lower in name_lower or difflib.SequenceMatcher(None, search_lower, name_lower).ratio() > 0.6:
            matches.append(name)
    return matches

def kill_processes_by_name(processes, name):
    """
    Kills all processes with the given name.
    """
    try:
        for proc in processes:
            if proc[0] == name:
                for pid in proc[4]:
                    try:
                        psutil.Process(pid).terminate()
                        print(f"{GREEN}{BOLD}Killed process {name} (PID: {pid}).{RESET}")
                    except Exception as e:
                        print(f"{RED}{BOLD}Error killing process {name} (PID: {pid}): {e}{RESET}")
    except Exception as e:
        print(f"{RED}{BOLD}Error killing processes: {e}{RESET}")

def suspend_processes_by_name(processes, name):
    """
    Suspends all processes with the given name and tracks them.
    """
    try:
        for proc in processes:
            if proc[0] == name:
                for pid in proc[4]:
                    try:
                        psutil.Process(pid).suspend()
                        print(f"{GREEN}{BOLD}Suspended process {name} (PID: {pid}).{RESET}")
                        # Track suspended processes
                        if name not in suspended_processes:
                            suspended_processes[name] = []
                        suspended_processes[name].append(pid)
                    except Exception as e:
                        print(f"{RED}{BOLD}Error suspending process {name} (PID: {pid}): {e}{RESET}")
    except Exception as e:
        print(f"{RED}{BOLD}Error suspending processes: {e}{RESET}")

def display_suspended_processes():
    """
    Displays all processes currently suspended by the user.
    """
    if not suspended_processes:
        print(f"{YELLOW}{BOLD}No processes are currently suspended by you.{RESET}")
        return

    print(f"\n{BOLD}{WHITE}{'Process Name':<30} {'Suspended PIDs':<20}{RESET}")
    for name, pids in suspended_processes.items():
        print(f"{name:<30} {', '.join(map(str, pids))}")

def resume_processes_by_name(name):
    """
    Resumes all processes with the given name that were suspended by the user.
    """
    if name not in suspended_processes:
        print(f"{YELLOW}{BOLD}No suspended processes found for '{name}'.{RESET}")
        return

    for pid in suspended_processes[name]:
        try:
            psutil.Process(pid).resume()
            print(f"{GREEN}{BOLD}Resumed process {name} (PID: {pid}).{RESET}")
        except Exception as e:
            print(f"{RED}{BOLD}Error resuming process {name} (PID: {pid}): {e}{RESET}")

    # Remove the process from the suspended list
    del suspended_processes[name]

def main():
    """
    Main loop: display processes and prompt for commands.
    """
    while True:
        print("\n" + "=" * 80)
        processes = get_windows_processes()
        processes_sorted = display_processes(processes)

        print(f"\n{BOLD}Commands:{RESET}")
        print(f"{CYAN}kill <name>{RESET} - Kill processes by name.")
        print(f"{CYAN}suspend <name>{RESET} - Suspend processes by name.")
        print(f"{CYAN}resume{RESET} - Resume suspended processes.")
        print(f"{CYAN}exit{RESET} - Quit the program.")

        user_input = input(f"\n{BOLD}Enter command: {RESET}").strip().lower()
        if user_input == "exit":
            print(f"{GREEN}{BOLD}Exiting...{RESET}")
            break
        elif user_input.startswith("kill "):
            search_term = user_input[5:].strip()
            matches = find_matching_processes(processes_sorted, search_term)
            if not matches:
                print(f"{YELLOW}{BOLD}No processes found matching '{search_term}'.{RESET}")
            else:
                for name in matches:
                    kill_processes_by_name(processes_sorted, name)
        elif user_input.startswith("suspend "):
            search_term = user_input[8:].strip()
            matches = find_matching_processes(processes_sorted, search_term)
            if not matches:
                print(f"{YELLOW}{BOLD}No processes found matching '{search_term}'.{RESET}")
            else:
                for name in matches:
                    suspend_processes_by_name(processes_sorted, name)
                # Display suspended processes after suspending
                display_suspended_processes()
        elif user_input == "resume":
            if not suspended_processes:
                print(f"{YELLOW}{BOLD}No processes are currently suspended by you.{RESET}")
            else:
                display_suspended_processes()
                name = input(f"{BOLD}Enter the name of the process to resume: {RESET}").strip()
                resume_processes_by_name(name)
        else:
            print(f"{RED}{BOLD}Invalid command. Try again.{RESET}")

        time.sleep(1)

if __name__ == "__main__":
    main()
