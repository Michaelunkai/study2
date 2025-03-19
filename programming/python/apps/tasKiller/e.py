import subprocess
import time
import psutil
import os
import shutil
from collections import defaultdict
import difflib

# Optional: Try importing pyfiglet for bulkier fonts.
try:
    import pyfiglet
    USE_PYFIGLET = True
except ImportError:
    USE_PYFIGLET = False

# Optional: Try importing win32gui, win32con and win32process to hide/show windows.
try:
    import win32gui
    import win32con
    try:
        import win32process
    except ImportError:
        win32process = None
    USE_WIN32 = True
except ImportError:
    USE_WIN32 = False

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
    Displays overall system CPU and memory usage using a bulkier font if available.
    """
    overall_cpu = psutil.cpu_percent(interval=0.1)
    overall_mem = psutil.virtual_memory().percent
    overview_text = f"Overall CPU Usage: {overall_cpu:.1f}%   Overall Memory Usage: {overall_mem:.1f}%"
    if USE_PYFIGLET:
        figlet = pyfiglet.Figlet(font="big")
        ascii_text = figlet.renderText(overview_text)
        print(ascii_text)
    else:
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

def show_process_details(process_tuple):
    """
    Displays detailed information for one process instance from the aggregated tuple.
    """
    name, count, cpu, mem, pids = process_tuple
    pid = pids[0]
    try:
        proc = psutil.Process(pid)
        details = {
            "Name": proc.name(),
            "PID": proc.pid,
            "Status": proc.status(),
            "Executable": proc.exe(),
            "Command Line": " ".join(proc.cmdline()),
            "Username": proc.username(),
            "Creation Time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(proc.create_time())),
            "CPU Times": proc.cpu_times(),
            "Memory Info": proc.memory_info(),
            "Number of Threads": proc.num_threads()
        }
        print(f"\n{BOLD}{UNDERLINE}Details for process '{name}' (PID {pid}):{RESET}")
        for key, value in details.items():
            print(f"{BOLD}{key}:{RESET} {value}")
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
        print(f"{RED}{BOLD}Unable to retrieve details for PID {pid}: {e}{RESET}")

def kill_process_by_pid():
    """
    Kills a process based on a user-entered PID.
    """
    pid_input = input(f"{BOLD}Enter PID to kill: {RESET}").strip()
    try:
        pid = int(pid_input)
        proc = psutil.Process(pid)
        proc.kill()
        print(f"{GREEN}{BOLD}Process with PID {pid} killed successfully.{RESET}")
    except ValueError:
        print(f"{RED}{BOLD}Invalid PID entered.{RESET}")
    except Exception as e:
        print(f"{RED}{BOLD}Failed to kill process with PID {pid_input}: {e}{RESET}")

def change_process_priority_by_index(process_tuple):
    """
    Changes the priority for the selected process.
    """
    name, count, cpu, mem, pids = process_tuple
    pid = pids[0]
    try:
        proc = psutil.Process(pid)
        print(f"Current priority for {name} (PID {pid}): {proc.nice()}")
        print("Choose new priority:")
        priorities = {
            "1": psutil.IDLE_PRIORITY_CLASS,
            "2": psutil.BELOW_NORMAL_PRIORITY_CLASS,
            "3": psutil.NORMAL_PRIORITY_CLASS,
            "4": psutil.ABOVE_NORMAL_PRIORITY_CLASS,
            "5": psutil.HIGH_PRIORITY_CLASS,
            "6": psutil.REALTIME_PRIORITY_CLASS,
        }
        print("1: IDLE, 2: BELOW NORMAL, 3: NORMAL, 4: ABOVE NORMAL, 5: HIGH, 6: REALTIME")
        choice = input("Enter choice (1-6): ").strip()
        if choice in priorities:
            proc.nice(priorities[choice])
            print(f"{GREEN}{BOLD}Priority changed for process {name} (PID {pid}).{RESET}")
        else:
            print(f"{YELLOW}{BOLD}Invalid choice. No changes made.{RESET}")
    except Exception as e:
        print(f"{RED}{BOLD}Failed to change priority for PID {pid}: {e}{RESET}")

def show_process_tree(process_tuple):
    """
    Displays the process tree (parent and child processes) for the selected process.
    """
    name, count, cpu, mem, pids = process_tuple
    pid = pids[0]
    try:
        proc = psutil.Process(pid)
        parent = proc.parent()
        children = proc.children(recursive=True)
        print(f"\n{BOLD}{UNDERLINE}Process Tree for '{name}' (PID {pid}):{RESET}")
        if parent:
            print(f"Parent: {parent.name()} (PID {parent.pid})")
        else:
            print("Parent: None")
        if children:
            print("Children:")
            for child in children:
                print(f"  - {child.name()} (PID {child.pid})")
        else:
            print("Children: None")
    except Exception as e:
        print(f"{RED}{BOLD}Failed to retrieve process tree for PID {pid}: {e}{RESET}")

def show_process_environ(process_tuple):
    """
    Displays the environment variables for the selected process.
    """
    name, count, cpu, mem, pids = process_tuple
    pid = pids[0]
    try:
        proc = psutil.Process(pid)
        env = proc.environ()
        print(f"\n{BOLD}{UNDERLINE}Environment Variables for '{name}' (PID {pid}):{RESET}")
        for key, value in env.items():
            print(f"{key} = {value}")
    except Exception as e:
        print(f"{RED}{BOLD}Failed to retrieve environment variables for PID {pid}: {e}{RESET}")

def get_hwnds_for_pid(pid):
    """
    Returns a list of window handles for the given process ID.
    Tries win32gui.GetWindowThreadProcessId; if not available, falls back to win32process.
    """
    hwnds = []
    def callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            try:
                # Try using win32gui's function
                _, found_pid = win32gui.GetWindowThreadProcessId(hwnd)
            except AttributeError:
                # Fall back to win32process if available
                if win32process:
                    _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                else:
                    found_pid = None
            if found_pid == pid:
                extra.append(hwnd)
        return True
    win32gui.EnumWindows(callback, hwnds)
    return hwnds

def toggle_suspend_resume(process_tuple):
    """
    Toggles suspend/resume for the selected process.
    Press 's' to suspend (hide its window so it stops appearing and using CPU),
    or 'r' to resume (restore its window).
    """
    name, count, cpu, mem, pids = process_tuple
    pid = pids[0]
    try:
        proc = psutil.Process(pid)
        action = input(f"Enter 's' to suspend (hide window) or 'r' to resume process {name} (PID {pid}): ").strip().lower()
        if action == 's':
            if USE_WIN32:
                hwnds = get_hwnds_for_pid(pid)
                for hwnd in hwnds:
                    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
            proc.suspend()
            print(f"{GREEN}{BOLD}Process {name} (PID {pid}) suspended and hidden.{RESET}")
        elif action == 'r':
            proc.resume()
            if USE_WIN32:
                hwnds = get_hwnds_for_pid(pid)
                for hwnd in hwnds:
                    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
            print(f"{GREEN}{BOLD}Process {name} (PID {pid}) resumed and its window restored.{RESET}")
        else:
            print(f"{YELLOW}{BOLD}Invalid action. No changes made.{RESET}")
    except Exception as e:
        print(f"{RED}{BOLD}Failed to toggle suspend/resume for PID {pid}: {e}{RESET}")

def list_process_threads(process_tuple):
    """
    Lists all threads for the selected process.
    """
    name, count, cpu, mem, pids = process_tuple
    pid = pids[0]
    try:
        proc = psutil.Process(pid)
        threads = proc.threads()
        print(f"\n{BOLD}{UNDERLINE}Threads for process '{name}' (PID {pid}):{RESET}")
        if threads:
            for t in threads:
                print(f"Thread ID: {t.id}, User Time: {t.user_time}, System Time: {t.system_time}")
        else:
            print("No threads found.")
    except Exception as e:
        print(f"{RED}{BOLD}Failed to list threads for PID {pid}: {e}{RESET}")

def print_menu():
    """
    Displays the command menu with one-letter shortcuts.
    """
    menu = f"""
{BOLD}{CYAN}Options:
[K] Kill by index (enter numbers, e.g. 1,3,5)
[S] Search processes
[D] Show process details
[P] Kill by PID
[N] Change process priority
[T] Show process tree
[V] Show environment variables
[X] Suspend/Resume a process (s: suspend/hide, r: resume/show)
[L] List process threads
[E] Exit{RESET}
"""
    print(menu)

def main():
    """
    Main loop: displays a title, process list, system overview, and a one-letter command menu.
    """
    while True:
        print("\n" + "=" * 80)
        title_text = "Process Monitor"
        if USE_PYFIGLET:
            figlet = pyfiglet.Figlet(font="big")
            print(figlet.renderText(title_text))
        else:
            print(f"{BOLD}{CYAN}{title_text}{RESET}")
        processes = get_windows_processes()
        processes_sorted = display_processes(processes)
        display_system_overview()
        print_menu()
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
            display_system_overview()
            kill_processes_by_image(filtered_sorted)
        elif command == "d":
            proc_num = input(f"{BOLD}Enter the process number for details: {RESET}").strip()
            try:
                idx = int(proc_num) - 1
                if idx < 0 or idx >= len(processes_sorted):
                    print(f"{RED}{BOLD}Index {proc_num} out of range.{RESET}")
                    continue
                show_process_details(processes_sorted[idx])
            except ValueError:
                print(f"{RED}{BOLD}Invalid input. Please enter a valid number.{RESET}")
        elif command == "p":
            kill_process_by_pid()
        elif command == "n":
            proc_num = input(f"{BOLD}Enter the process number to change priority: {RESET}").strip()
            try:
                idx = int(proc_num) - 1
                if idx < 0 or idx >= len(processes_sorted):
                    print(f"{RED}{BOLD}Index {proc_num} out of range.{RESET}")
                    continue
                change_process_priority_by_index(processes_sorted[idx])
            except ValueError:
                print(f"{RED}{BOLD}Invalid input. Please enter a valid number.{RESET}")
        elif command == "t":
            proc_num = input(f"{BOLD}Enter the process number for tree view: {RESET}").strip()
            try:
                idx = int(proc_num) - 1
                if idx < 0 or idx >= len(processes_sorted):
                    print(f"{RED}{BOLD}Index {proc_num} out of range.{RESET}")
                    continue
                show_process_tree(processes_sorted[idx])
            except ValueError:
                print(f"{RED}{BOLD}Invalid input. Please enter a valid number.{RESET}")
        elif command == "v":
            proc_num = input(f"{BOLD}Enter the process number to show environment variables: {RESET}").strip()
            try:
                idx = int(proc_num) - 1
                if idx < 0 or idx >= len(processes_sorted):
                    print(f"{RED}{BOLD}Index {proc_num} out of range.{RESET}")
                    continue
                show_process_environ(processes_sorted[idx])
            except ValueError:
                print(f"{RED}{BOLD}Invalid input. Please enter a valid number.{RESET}")
        elif command == "x":
            proc_num = input(f"{BOLD}Enter the process number to suspend/resume: {RESET}").strip()
            try:
                idx = int(proc_num) - 1
                if idx < 0 or idx >= len(processes_sorted):
                    print(f"{RED}{BOLD}Index {proc_num} out of range.{RESET}")
                    continue
                toggle_suspend_resume(processes_sorted[idx])
            except ValueError:
                print(f"{RED}{BOLD}Invalid input. Please enter a valid number.{RESET}")
        elif command == "l":
            proc_num = input(f"{BOLD}Enter the process number to list threads: {RESET}").strip()
            try:
                idx = int(proc_num) - 1
                if idx < 0 or idx >= len(processes_sorted):
                    print(f"{RED}{BOLD}Index {proc_num} out of range.{RESET}")
                    continue
                list_process_threads(processes_sorted[idx])
            except ValueError:
                print(f"{RED}{BOLD}Invalid input. Please enter a valid number.{RESET}")
        elif command.isdigit() or ("," in command and all(x.strip().isdigit() for x in command.split(","))):
            kill_processes_by_image(processes_sorted)
        else:
            print(f"{YELLOW}{BOLD}Unknown command. Please try again.{RESET}")
        time.sleep(1)

if __name__ == "__main__":
    main()

