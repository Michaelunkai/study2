import subprocess
import time
import psutil
import os
import shutil
from collections import defaultdict
import difflib
import glob
import re
import pyreadline as readline  # For command history

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

# Command history file
HISTORY_FILE = os.path.join(os.path.expanduser("~"), ".process_monitor_history")

# Predefined applications
PREDEFINED_APPS = [
    "WeMod",
    "JoyToKey",
    "Spider",
    "Ludusavi",
    "OBS",
    "SuperF4"
]

def setup_history():
    """Set up command history with pyreadline"""
    # Create history file if it doesn't exist
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'w') as f:
            pass
    
    # Configure readline
    try:
        # Load history from file
        if os.path.exists(HISTORY_FILE) and os.path.getsize(HISTORY_FILE) > 0:
            with open(HISTORY_FILE, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        readline.add_history(line)
        
        # Set history length
        readline.set_history_length(1000)  # Increased history size
    except Exception as e:
        print(f"{YELLOW}Warning: Could not set up history: {e}{RESET}")

def save_history():
    """Save command history to file"""
    try:
        # Get current history
        history_length = readline.get_current_history_length()
        history_items = [readline.get_history_item(i) for i in range(1, history_length + 1)]
        
        # Filter out None values and empty strings
        history_items = [item for item in history_items if item and item.strip()]
        
        # Write to file
        with open(HISTORY_FILE, 'w') as f:
            for item in history_items:
                f.write(f"{item}\n")
    except Exception as e:
        print(f"{YELLOW}Warning: Could not save history: {e}{RESET}")

def add_to_history(command):
    """Add command to history if it's not empty"""
    if command and command.strip():
        try:
            readline.add_history(command)
        except Exception:
            pass

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
    processes_sorted = [proc for _, proc in sorted(processes_with_score, key=lambda x: x[0], reverse=True)]
    
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

def normalize_name(name):
    """
    Normalizes a name for better fuzzy matching by removing common separators and converting to lowercase.
    """
    return re.sub(r'[_\-.\s]', '', name.lower())

def is_name_match(search_term, name, min_similarity=0.6):
    """
    Determines if a name matches a search term using various matching strategies.
    Returns True if it's a match, False otherwise.
    """
    # Remove file extension for better matching
    if name.lower().endswith('.exe') or name.lower().endswith('.lnk'):
        name_without_ext = os.path.splitext(name)[0]
    else:
        name_without_ext = name
    
    # Normalize both terms
    term_norm = normalize_name(search_term)
    name_norm = normalize_name(name_without_ext)
    
    # Direct substring match (case insensitive)
    if term_norm in name_norm:
        # If search term is a substring of the name, it's a strong match
        # Calculate what percentage of the name is matched
        match_ratio = len(term_norm) / len(name_norm) if name_norm else 0
        if match_ratio > 0.3:  # If search term is at least 30% of the name
            return True
    
    # Check if name is a substring of search term (e.g., "man" in "spiderman")
    if name_norm in term_norm and len(name_norm) > 2:  # Avoid matching very short substrings
        return True
    
    # For game titles, check if search term matches the main part of the game name
    # Example: "spider" should match "Spider-Man 2"
    name_parts = re.split(r'[-_\s]', name_without_ext.lower())
    term_parts = re.split(r'[-_\s]', search_term.lower())
    
    # Check if any significant part matches
    for part in name_parts:
        if len(part) >= 3:  # Only consider significant parts
            for term_part in term_parts:
                if len(term_part) >= 3 and (term_part in part or part in term_part):
                    return True
    
    # Sequence matcher for overall similarity
    seq_ratio = difflib.SequenceMatcher(None, term_norm, name_norm).ratio()
    if seq_ratio >= min_similarity:
        return True
    
    # Check for common words (especially useful for game titles)
    term_words = set(re.findall(r'\w+', search_term.lower()))
    name_words = set(re.findall(r'\w+', name_without_ext.lower()))
    
    # If there are common significant words
    common_words = term_words.intersection(name_words)
    if common_words and any(len(word) >= 4 for word in common_words):
        return True
    
    return False

def calculate_similarity(term, name):
    """
    Calculates similarity between search term and name using multiple methods.
    Returns a similarity score between 0 and 1.
    """
    # Remove file extension for better matching
    if name.lower().endswith('.exe') or name.lower().endswith('.lnk'):
        name_without_ext = os.path.splitext(name)[0]
    else:
        name_without_ext = name
    
    term_norm = normalize_name(term)
    name_norm = normalize_name(name_without_ext)
    
    # Direct substring match
    if term_norm in name_norm:
        # Calculate what percentage of the name is matched
        match_ratio = len(term_norm) / len(name_norm) if name_norm else 0
        return max(0.7, 0.5 + match_ratio)  # Higher score for better coverage
    
    if name_norm in term_norm and len(name_norm) > 2:
        return 0.7
    
    # For game titles, check if search term matches the main part of the game name
    name_parts = re.split(r'[-_\s]', name_without_ext.lower())
    term_parts = re.split(r'[-_\s]', term.lower())
    
    # Check if any significant part matches
    for part in name_parts:
        if len(part) >= 3:  # Only consider significant parts
            for term_part in term_parts:
                if len(term_part) >= 3 and (term_part in part or part in term_part):
                    return 0.8
    
    # Sequence matcher for fuzzy matching
    seq_ratio = difflib.SequenceMatcher(None, term_norm, name_norm).ratio()
    
    # Check for common words
    term_words = set(re.findall(r'\w+', term.lower()))
    name_words = set(re.findall(r'\w+', name_without_ext.lower()))
    common_words = term_words.intersection(name_words)
    
    # If there are common significant words
    if common_words and any(len(word) >= 4 for word in common_words):
        word_ratio = len(common_words) / max(len(term_words), 1)
        return max(0.6, word_ratio)
    
    # Return the sequence ratio
    return seq_ratio

def search_processes(processes, search_term):
    """
    Filters the process list based on a search term using fuzzy matching.
    Uses more lenient matching for better results.
    """
    filtered = []
    search_lower = search_term.lower()
    
    for proc in processes:
        name, count, cpu, mem, pids = proc
        
        # Check if name matches search term
        if is_name_match(search_term, name, min_similarity=0.5):
            filtered.append(proc)
            continue
        
        # Check command line for additional matching
        try:
            proc_obj = psutil.Process(pids[0])
            cmdline = " ".join(proc_obj.cmdline()).lower()
            if search_lower in cmdline:
                filtered.append(proc)
                continue
        except Exception:
            pass
    
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

def parse_multiple_terms(input_str):
    """
    Parses input string to extract multiple terms.
    Handles various separators: spaces, commas, angle brackets.
    """
    # Replace angle brackets with spaces and split by spaces or commas
    terms = re.findall(r'<([^>]+)>|([^,\s<>]+)', input_str)
    
    # Flatten the list of tuples and filter out empty strings
    result = []
    for t in terms:
        term = t[0] if t[0] else t[1]
        if term.strip():
            result.append(term.strip())
    
    return result

def search_and_kill(processes_sorted, search_terms):
    """
    Searches for and kills processes matching multiple search terms.
    """
    terms = parse_multiple_terms(search_terms)
    
    if not terms:
        print(f"{YELLOW}{BOLD}No search terms provided.{RESET}")
        return
    
    all_matching = []
    for term in terms:
        filtered = search_processes(processes_sorted, term)
        if filtered:
            print(f"\n{CYAN}{BOLD}Found processes matching '{term}':{RESET}")
            display_processes(filtered)
            all_matching.extend(filtered)
        else:
            print(f"{YELLOW}{BOLD}No processes matching '{term}' found.{RESET}")
    
    if all_matching:
        print(f"\n{YELLOW}{BOLD}Killing all matched processes...{RESET}")
        kill_processes_by_image(all_matching)

def find_executable_paths(search_term, min_similarity=0.6, max_results=10):
    """
    Finds executable paths that match the search term using fuzzy matching.
    Returns a list of tuples: (similarity_score, full_path, file_name)
    """
    common_paths = [
        'C:\\Games\\',
        'C:\\Program Files\\Steam\\steamapps\\common\\',
        'C:\\Program Files (x86)\\Steam\\steamapps\\common\\',
        'D:\\Games\\',
        'D:\\Steam\\steamapps\\common\\',
        'E:\\Games\\',
        os.path.join(os.environ.get('ProgramFiles', 'C:\\Program Files'), ''),
        os.path.join(os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)'), ''),
        os.path.join(os.environ.get('LOCALAPPDATA', ''), ''),
        os.path.join(os.environ.get('APPDATA', ''), ''),
        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs'),
        # Add more common game/app installation paths as needed
    ]
    
    # Add Windows Start Menu paths
    start_menu_paths = [
        os.path.join(os.environ.get('ProgramData', ''), 'Microsoft', 'Windows', 'Start Menu', 'Programs'),
        os.path.join(os.environ.get('APPDATA', ''), 'Microsoft', 'Windows', 'Start Menu', 'Programs')
    ]
    common_paths.extend([p for p in start_menu_paths if os.path.exists(p)])
    
    matches = []
    
    # Search for .exe files in common paths
    for base_path in common_paths:
        if not os.path.exists(base_path):
            continue
            
        # Use glob to find all .exe files (faster than os.walk for shallow searches)
        for pattern in ['*.exe', '*/*.exe', '*/*/*.exe']:
            try:
                for exe_path in glob.glob(os.path.join(base_path, pattern)):
                    file_name = os.path.basename(exe_path)
                    
                    # Check if name matches search term
                    if is_name_match(search_term, file_name, min_similarity):
                        similarity = calculate_similarity(search_term, file_name)
                        matches.append((similarity, exe_path, file_name))
            except Exception:
                continue
                
        # For deeper searches, use os.walk but limit depth
        depth = 0
        for root, dirs, files in os.walk(base_path):
            # Limit search depth to avoid excessive scanning
            if depth > 3:
                continue
                
            for file in files:
                if file.lower().endswith('.exe'):
                    full_path = os.path.join(root, file)
                    
                    # Check if name matches search term
                    if is_name_match(search_term, file, min_similarity):
                        similarity = calculate_similarity(search_term, file)
                        matches.append((similarity, full_path, file))
            
            depth += 1
    
    # Search for .lnk files in Start Menu (shortcuts to applications)
    for base_path in start_menu_paths:
        if not os.path.exists(base_path):
            continue
            
        for root, _, files in os.walk(base_path):
            for file in files:
                if file.lower().endswith('.lnk'):
                    shortcut_name = os.path.splitext(file)[0]
                    
                    # Check if name matches search term
                    if is_name_match(search_term, shortcut_name, min_similarity):
                        similarity = calculate_similarity(search_term, shortcut_name)
                        full_path = os.path.join(root, file)
                        matches.append((similarity, full_path, shortcut_name + '.lnk'))
    
    # Sort by similarity score and return top matches
    return sorted(matches, key=lambda x: x[0], reverse=True)[:max_results]

def run_application(search_terms):
    """
    Searches for and runs applications based on fuzzy name matching.
    Automatically runs all matching applications without asking for confirmation.
    Only runs applications with names very similar to the search term.
    """
    terms = parse_multiple_terms(search_terms)
    
    if not terms:
        print(f"{YELLOW}{BOLD}No search terms provided.{RESET}")
        return
    
    # Process each term individually
    found_any = False
    for term in terms:
        # Find matches with higher similarity threshold (0.6) to ensure only closely matching apps are found
        matches = find_executable_paths(term, min_similarity=0.6, max_results=5)
        
        if matches:
            found_any = True
            print(f"\n{CYAN}{BOLD}Found matches for '{term}':{RESET}")
            
            # Display all matches
            for i, (similarity, path, name) in enumerate(matches, 1):
                similarity_percent = int(similarity * 100)
                print(f"{i}. {name} ({similarity_percent}% match)")
                print(f"   Path: {path}")
            
            # Filter out uninstaller and setup executables
            filtered_matches = []
            for match in matches:
                similarity, path, name = match
                name_lower = name.lower()
                
                # Skip uninstallers, setup files, and other utility executables
                if any(keyword in name_lower for keyword in ['uninstall', 'setup', 'installer', 'remove', 'update']):
                    print(f"{YELLOW}Skipping utility executable: {name}{RESET}")
                    continue
                
                filtered_matches.append(match)
            
            # Run all remaining matches automatically
            if filtered_matches:
                print(f"\n{GREEN}{BOLD}Automatically running all matching applications for '{term}'...{RESET}")
                
                for similarity, path, name in filtered_matches:
                    try:
                        print(f"{GREEN}Starting {name}...{RESET}")
                        subprocess.Popen(path, shell=True)
                        time.sleep(0.5)  # Brief pause between launches
                    except Exception as e:
                        print(f"{RED}{BOLD}Error running {name}: {e}{RESET}")
            else:
                print(f"{YELLOW}{BOLD}No suitable applications to run for '{term}' after filtering.{RESET}")
        else:
            print(f"{YELLOW}{BOLD}No matches found for '{term}'{RESET}")
    
    if not found_any:
        print(f"{YELLOW}{BOLD}No matching applications found for any search term.{RESET}")

def run_predefined_apps():
    """
    Runs all predefined applications.
    """
    print(f"{CYAN}{BOLD}Running predefined applications...{RESET}")
    for app in PREDEFINED_APPS:
        try:
            print(f"{GREEN}Looking for {app}...{RESET}")
            run_application(app)
            time.sleep(1)  # Add a small delay between launching apps
        except Exception as e:
            print(f"{RED}{BOLD}Error running {app}: {e}{RESET}")

def close_predefined_apps():
    """
    Closes all predefined applications.
    """
    print(f"{CYAN}{BOLD}Closing predefined applications...{RESET}")
    processes = get_windows_processes()
    processes_to_kill = []
    
    for app in PREDEFINED_APPS:
        filtered = search_processes(processes, app)
        if filtered:
            print(f"{YELLOW}Found processes matching '{app}':{RESET}")
            for proc in filtered:
                name, count, _, _, _ = proc
                print(f"- {name} ({count} instances)")
            processes_to_kill.extend(filtered)
        else:
            print(f"{YELLOW}No processes matching '{app}' found.{RESET}")
    
    if processes_to_kill:
        print(f"\n{YELLOW}{BOLD}Closing all matched applications...{RESET}")
        kill_processes_by_image(processes_to_kill)
    else:
        print(f"{YELLOW}{BOLD}No predefined applications are currently running.{RESET}")

def main():
    """
    Main loop: displays process list, system overview, and search option.
    """
    # Set up command history
    setup_history()
    
    try:
        # Configure pyreadline for better history navigation
        # This helps with PageUp/PageDown functionality
        if hasattr(readline, 'set_startup_hook'):
            readline.set_startup_hook(lambda: None)
        
        # Enable history search with PageUp/PageDown
        if hasattr(readline, 'parse_and_bind'):
            readline.parse_and_bind('"\e[5~": previous-history')  # PageUp
            readline.parse_and_bind('"\e[6~": next-history')      # PageDown
        
        while True:
            print("\n" + "=" * 80)
            print(f"{BOLD}{CYAN}Process Monitor{RESET}")
            processes = get_windows_processes()
            processes_sorted = display_processes(processes)
            display_system_overview()
            print(f"\n{BOLD}{CYAN}Options:{RESET}")
            print(f"{BOLD}[S] Search and kill processes (separate multiple with space/comma/<>){RESET}")
            print(f"{BOLD}[U] Run applications (separate multiple with space/comma/<>){RESET}")
            print(f"{BOLD}[numbers] Enter process numbers to kill (e.g. 1,5,111){RESET}")
            print(f"{BOLD}[G] Run all predefined applications (WeMod, JoyToKey, Spider, Ludusavi, OBS, SuperF4){RESET}")
            print(f"{BOLD}[C] Close all predefined applications{RESET}")
            print(f"{BOLD}[E] Exit{RESET}")
            
            command = input(f"{BOLD}Enter option: {RESET}").strip().lower()
            
            # Add command to history
            add_to_history(command)
            
            if command == "e":
                print(f"{GREEN}{BOLD}Exiting...{RESET}")
                break
            elif command == "s":
                terms = input(f"{BOLD}Enter search terms: {RESET}").strip()
                add_to_history(terms)  # Add search terms to history
                if terms:
                    search_and_kill(processes_sorted, terms)
            elif command == "u":
                terms = input(f"{BOLD}Enter application names: {RESET}").strip()
                add_to_history(terms)  # Add application names to history
                if terms:
                    run_application(terms)
            elif command.replace(",", "").replace(" ", "").isdigit():
                kill_processes_by_indices(processes_sorted, command)
            elif command == "g":
                run_predefined_apps()
            elif command == "c":
                close_predefined_apps()
            else:
                print(f"{YELLOW}{BOLD}Unknown command. Please try again.{RESET}")
            
            # Save history after each command
            save_history()
            
            time.sleep(1)
    finally:
        # Save command history when exiting
        save_history()

if __name__ == "__main__":
    main()
