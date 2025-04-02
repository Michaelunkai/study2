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
    Processes are sorted by combined CPU and memory usage (normalized).
    Processes matching important system names are highlighted in red.
    Returns the sorted list.
    """
    # Normalize and combine CPU and memory metrics
    max_cpu = max(cpu for _, _, cpu, _, _ in processes) if processes else 1
    max_mem = max(mem for _, _, _, mem, _ in processes) if processes else 1
    
    # Create list with normalized scores
    processes_with_score = []
    for proc in processes:
        name, count, cpu, mem, pids = proc
        cpu_norm = cpu / max_cpu if max_cpu > 0 else 0
        mem_norm = mem / max_mem if max_mem > 0 else 0
        combined_score = cpu_norm + mem_norm
        processes_with_score.append((combined_score, proc))
    
    # Sort by combined score
    processes_sorted = [proc for _, proc in sorted(processes_with_score, key=lambda x: x[0])]
    
    try:
        terminal_width = shutil.get_terminal_size().columns
    except Exception:
        terminal_width = 100
        
    header = f"{BOLD}{UNDERLINE}{WHITE}{'No.':<4} {'Process Name':<30} {'Instances':<10} {'CPU (%)':<10} {'Memory (MB)':<12} {'Usage Score':<10}{RESET}"
    print(header)
    
    for idx, (name, count, cpu, mem, pids) in enumerate(processes_sorted, start=1):
        cpu_norm = cpu / max_cpu if max_cpu > 0 else 0
        mem_norm = mem / max_mem if max_mem > 0 else 0
        score = cpu_norm + mem_norm
        
        idx_str = f"{idx:<4}"
        name_str = f"{name:<30}"
        count_str = f"{count:<10}"
        cpu_str = f"{cpu:.2f}".rjust(10)
        mem_str = f"{mem:.2f}".rjust(12)
        score_str = f"{score:.3f}".rjust(10)
        
        color = RED if name.lower() in IMPORTANT_PROCESSES else RESET
        print(f"{idx_str} {color}{name_str}{RESET} {count_str} {cpu_str} {mem_str} {score_str}")
    
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
    Uses more lenient matching for better results.
    """
    filtered = []
    search_lower = search_term.lower()
    
    for proc in processes:
        name, count, cpu, mem, pids = proc
        name_lower = name.lower()
        
        # More lenient matching criteria
        name_match = (
            search_lower in name_lower or  # Direct substring match
            name_lower in search_lower or  # Reverse substring match
            difflib.SequenceMatcher(None, search_lower, name_lower).ratio() > 0.4  # Lower threshold
        )
        
        cmdline_match = False
        try:
            proc_obj = psutil.Process(pids[0])
            cmdline = " ".join(proc_obj.cmdline()).lower()
            cmdline_match = search_lower in cmdline
        except Exception:
            pass
            
        if name_match or cmdline_match:
            filtered.append(proc)
    return filtered

def kill_processes_by_image(processes_to_kill):
    """
    Kills all the processes in the provided list along with their child processes.
    """
    if not processes_to_kill:
        print(f"{YELLOW}{BOLD}No processes found to kill.{RESET}")
        return

    # Collect all related processes and children
    all_process_names = set()
    all_pids = set()
    
    # First, collect all direct matches
    for proc in processes_to_kill:
        name, _, _, _, pids = proc
        all_process_names.add(name)
        all_pids.update(pids)
    
    # Then collect all child processes
    child_pids = set()
    for pid in all_pids:
        try:
            proc = psutil.Process(pid)
            children = proc.children(recursive=True)
            for child in children:
                child_pids.add(child.pid)
                all_process_names.add(child.name())
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    all_pids.update(child_pids)
    
    # Kill by image name first (tends to be more thorough)
    for name in all_process_names:
        try:
            print(f"{YELLOW}{BOLD}Killing all processes with image name '{name}'...{RESET}")
            result = subprocess.run(
                ['taskkill.exe', '/F', '/IM', name],
                capture_output=True,
                text=True,
                check=False  # Don't throw error if some processes can't be killed
            )
            if result.returncode == 0:
                print(f"{GREEN}{BOLD}Successfully terminated processes with image name '{name}'.{RESET}")
            else:
                print(f"{YELLOW}{BOLD}Some processes with image name '{name}' could not be terminated.{RESET}")
        except Exception as e:
            print(f"{RED}{BOLD}Error killing processes with image name '{name}': {e}{RESET}")
    
    # Also try to kill by PID for any remaining processes
    for pid in all_pids:
        try:
            proc = psutil.Process(pid)
            proc_name = proc.name()
            print(f"{YELLOW}{BOLD}Killing process '{proc_name}' (PID {pid})...{RESET}")
            proc.kill()
            print(f"{GREEN}{BOLD}Process '{proc_name}' (PID {pid}) killed successfully.{RESET}")
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            print(f"{RED}{BOLD}Failed to kill process with PID {pid}: {e}{RESET}")

def kill_processes_by_indices(processes_sorted, indices_str):
    """
    Kills processes by their display indices.
    """
    try:
        # Parse the indices, handling comma-separated and space-separated values
        parts = indices_str.replace(",", " ").split()
        indices = []
        
        for part in parts:
            try:
                idx = int(part) - 1  # Convert to 0-based index
                if idx < 0 or idx >= len(processes_sorted):
                    print(f"{RED}{BOLD}Index {part} out of range.{RESET}")
                    continue
                indices.append(idx)
            except ValueError:
                print(f"{RED}{BOLD}Invalid number: {part}.{RESET}")
                continue
        
        if not indices:
            print(f"{YELLOW}{BOLD}No valid process indices provided.{RESET}")
            return
        
        # Get the processes to kill
        processes_to_kill = [processes_sorted[idx] for idx in indices]
        
        # Confirm killing
        names = [proc[0] for proc in processes_to_kill]
        print(f"{YELLOW}{BOLD}You are about to kill these processes and all related processes:{RESET}")
        for name in names:
            print(f"- {name}")
        
        # Kill the processes
        kill_processes_by_image(processes_to_kill)
        
    except Exception as e:
        print(f"{RED}{BOLD}Error processing indices: {e}{RESET}")

def search_and_kill(processes_sorted, search_term):
    """
    Searches for processes matching the term and immediately kills them.
    """
    filtered_processes = search_processes(processes_sorted, search_term)
    if not filtered_processes:
        print(f"{YELLOW}{BOLD}No processes matching '{search_term}' found.{RESET}")
        return
    
    print(f"\n{CYAN}{BOLD}Found these processes matching '{search_term}':{RESET}")
    display_processes(filtered_processes)
    
    # Immediately kill all found processes
    print(f"{YELLOW}{BOLD}Killing all processes related to '{search_term}'...{RESET}")
    kill_processes_by_image(filtered_processes)

def main():
    """
    Main loop: displays process list and accepts search input by default.
    """
    while True:
        print("\n" + "=" * 80)
        print(f"{BOLD}{CYAN}Process Monitor{RESET}")
        processes = get_windows_processes()
        processes_sorted = display_processes(processes)
        display_system_overview()
        print(f"\n{BOLD}{CYAN}Options:{RESET}")
        print(f"{BOLD}Enter search term to find and kill processes{RESET}")
        print(f"{BOLD}[numbers] Enter process numbers to kill (e.g. 1,5,111){RESET}")
        print(f"{BOLD}[E] Exit{RESET}")
        
        command = input(f"{BOLD}Enter search or command: {RESET}").strip().lower()
        
        if command == "e":
            print(f"{GREEN}{BOLD}Exiting...{RESET}")
            break
        elif command.replace(",", "").replace(" ", "").isdigit():
            # Direct killing by indices
            kill_processes_by_indices(processes_sorted, command)
        elif command:  # Any non-empty input is treated as a search term
            search_and_kill(processes_sorted, command)
        
        time.sleep(1)

if __name__ == "__main__":
    main()