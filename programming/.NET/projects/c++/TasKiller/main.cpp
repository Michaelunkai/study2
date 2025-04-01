#include <windows.h>
#include <tlhelp32.h>
#include <psapi.h>
#include <iostream>
#include <iomanip>
#include <vector>
#include <string>
#include <map>
#include <algorithm>
#include <thread>
#include <chrono>
#include <cctype>
#include <sstream>

// ANSI escape codes (if your terminal supports them)
#define RED "\033[91m"
#define GREEN "\033[92m"
#define YELLOW "\033[93m"
#define CYAN "\033[96m"
#define WHITE "\033[97m"
#define BOLD "\033[1m"
#define UNDERLINE "\033[4m"
#define RESET "\033[0m"

// A set of important process names (in lowercase)
const std::vector<std::string> IMPORTANT_PROCESSES = {
    "system idle process", "system", "csrss.exe", "wininit.exe", "winlogon.exe",
    "services.exe", "lsass.exe", "smss.exe", "svchost.exe", "explorer.exe"
};

struct ProcessInfo {
    std::string name;
    int count;
    double cpu;     // Placeholder (requires time-differenced measurements)
    double memory;  // in MB
    std::vector<DWORD> pids;
};

// Utility: convert string to lowercase.
std::string toLower(const std::string& s) {
    std::string ret = s;
    std::transform(ret.begin(), ret.end(), ret.begin(), ::tolower);
    return ret;
}

// Check if a process name is in the important list.
bool isImportant(const std::string &name) {
    std::string lname = toLower(name);
    for (auto& imp : IMPORTANT_PROCESSES) {
        if(lname == imp)
            return true;
    }
    return false;
}

// Get list of processes and aggregate info by image name.
std::vector<ProcessInfo> getWindowsProcesses() {
    std::map<std::string, ProcessInfo> procMap;
    
    // Take a snapshot of all processes.
    HANDLE hSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (hSnap == INVALID_HANDLE_VALUE) {
        std::cerr << RED << BOLD << "Error taking process snapshot." << RESET << std::endl;
        return {};
    }
    
    PROCESSENTRY32 pe32;
    pe32.dwSize = sizeof(PROCESSENTRY32);
    if (!Process32First(hSnap, &pe32)) {
        std::cerr << RED << BOLD << "Error reading process snapshot." << RESET << std::endl;
        CloseHandle(hSnap);
        return {};
    }
    
    do {
        std::string procName = pe32.szExeFile;
        DWORD pid = pe32.th32ProcessID;
        // Open process to query memory info
        HANDLE hProc = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, FALSE, pid);
        double memMB = 0.0;
        if (hProc) {
            PROCESS_MEMORY_COUNTERS pmc;
            if (GetProcessMemoryInfo(hProc, &pmc, sizeof(pmc))) {
                memMB = static_cast<double>(pmc.WorkingSetSize) / (1024 * 1024);
            }
            CloseHandle(hProc);
        }
        
        // For this example, we leave CPU usage as 0.0
        double cpuUsage = 0.0;
        
        std::string key = toLower(procName);
        if (procMap.find(key) == procMap.end()) {
            ProcessInfo info;
            info.name = procName;
            info.count = 1;
            info.cpu = cpuUsage;
            info.memory = memMB;
            info.pids.push_back(pid);
            procMap[key] = info;
        } else {
            procMap[key].count++;
            procMap[key].cpu += cpuUsage;
            procMap[key].memory += memMB;
            procMap[key].pids.push_back(pid);
        }
        
    } while (Process32Next(hSnap, &pe32));
    
    CloseHandle(hSnap);
    
    std::vector<ProcessInfo> processes;
    for (auto &entry : procMap) {
        processes.push_back(entry.second);
    }
    return processes;
}

// Display the process list sorted by memory usage.
std::vector<ProcessInfo> displayProcesses(const std::vector<ProcessInfo>& processes) {
    auto procList = processes;
    std::sort(procList.begin(), procList.end(), [](const ProcessInfo& a, const ProcessInfo& b) {
        return a.memory < b.memory;
    });
    
    std::cout << BOLD << UNDERLINE << WHITE
              << std::setw(4) << "No." 
              << " " << std::setw(30) << "Process Name" 
              << " " << std::setw(10) << "Instances" 
              << " " << std::setw(10) << "CPU (%)" 
              << " " << std::setw(12) << "Memory (MB)"
              << RESET << std::endl;
    
    int index = 1;
    int totalInstances = 0;
    double totalMemory = 0.0;
    for (auto &proc : procList) {
        totalInstances += proc.count;
        totalMemory += proc.memory;
        std::string color = isImportant(proc.name) ? RED : RESET;
        std::cout << std::setw(4) << index << " " 
                  << color << std::setw(30) << proc.name << RESET << " "
                  << std::setw(10) << proc.count << " "
                  << std::setw(10) << std::fixed << std::setprecision(2) << proc.cpu << " "
                  << std::setw(12) << std::fixed << std::setprecision(2) << proc.memory 
                  << std::endl;
        index++;
    }
    std::cout << std::string(80, '-') << std::endl;
    std::cout << BOLD << "Total: " << procList.size() 
              << " unique processes, " << totalInstances 
              << " instances, " << std::fixed << std::setprecision(2) 
              << totalMemory << " MB used" << RESET << std::endl;
    
    return procList;
}

// Displays overall system memory usage (simplified)
void displaySystemOverview() {
    MEMORYSTATUSEX memStatus;
    memStatus.dwLength = sizeof(memStatus);
    GlobalMemoryStatusEx(&memStatus);
    double memUsage = (100.0 - (memStatus.ullAvailPhys * 100.0 / memStatus.ullTotalPhys));
    
    std::cout << BOLD << CYAN 
              << "Overall Memory Usage: " << std::fixed << std::setprecision(1) << memUsage << "%" 
              << RESET << std::endl;
}

// Very basic fuzzy search: substring matching in process name.
std::vector<ProcessInfo> searchProcesses(const std::vector<ProcessInfo>& processes, const std::string& term) {
    std::vector<ProcessInfo> filtered;
    std::string lowerTerm = toLower(term);
    for (const auto &proc : processes) {
        if (toLower(proc.name).find(lowerTerm) != std::string::npos)
            filtered.push_back(proc);
    }
    return filtered;
}

// Kill processes by image name (using TerminateProcess for each PID)
void killProcessesByImage(const std::vector<ProcessInfo>& processes) {
    std::cout << "\n" << BOLD << "Enter process numbers to kill (e.g. 1,3,5) or press Enter to cancel: " << RESET;
    std::string input;
    std::getline(std::cin, input);
    if (input.empty()) {
        std::cout << YELLOW << BOLD << "No processes selected for killing. Returning to main menu." << RESET << std::endl;
        return;
    }
    std::istringstream iss(input);
    std::string token;
    std::vector<int> indices;
    while (std::getline(iss, token, ',')) {
        try {
            int idx = std::stoi(token) - 1;
            if (idx < 0 || idx >= static_cast<int>(processes.size())) {
                std::cout << RED << BOLD << "Index " << token << " out of range." << RESET << std::endl;
                return;
            }
            indices.push_back(idx);
        } catch (...) {
            std::cout << RED << BOLD << "Invalid number: " << token << RESET << std::endl;
            return;
        }
    }
    
    for (int idx : indices) {
        const ProcessInfo &proc = processes[idx];
        bool success = true;
        for (DWORD pid : proc.pids) {
            HANDLE hProc = OpenProcess(PROCESS_TERMINATE, FALSE, pid);
            if (hProc) {
                if (!TerminateProcess(hProc, 1)) {
                    success = false;
                }
                CloseHandle(hProc);
            } else {
                success = false;
            }
        }
        if (success)
            std::cout << GREEN << BOLD << "Killed all processes with image name '" << proc.name << "'." << RESET << std::endl;
        else
            std::cout << RED << BOLD << "Error killing processes with image name '" << proc.name << "'." << RESET << std::endl;
    }
}

// Show process details for the first PID in the aggregated group.
void showProcessDetails(const ProcessInfo &proc) {
    if (proc.pids.empty()) {
        std::cout << RED << BOLD << "No PID available for process " << proc.name << RESET << std::endl;
        return;
    }
    DWORD pid = proc.pids[0];
    HANDLE hProc = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, FALSE, pid);
    if (!hProc) {
        std::cout << RED << BOLD << "Unable to open process " << pid << RESET << std::endl;
        return;
    }
    
    char exePath[MAX_PATH] = {0};
    GetModuleFileNameExA(hProc, NULL, exePath, MAX_PATH);
    
    FILETIME creationTime, exitTime, kernelTime, userTime;
    GetProcessTimes(hProc, &creationTime, &exitTime, &kernelTime, &userTime);
    
    SYSTEMTIME sysTime;
    FileTimeToSystemTime(&creationTime, &sysTime);
    
    std::cout << "\n" << BOLD << UNDERLINE 
              << "Details for process '" << proc.name << "' (PID " << pid << "):" 
              << RESET << std::endl;
    std::cout << BOLD << "Executable:" << RESET << " " << exePath << std::endl;
    std::cout << BOLD << "Creation Time:" << RESET << " " 
              << sysTime.wYear << "-" << sysTime.wMonth << "-" << sysTime.wDay << " " 
              << sysTime.wHour << ":" << sysTime.wMinute << ":" << sysTime.wSecond << std::endl;
    
    CloseHandle(hProc);
}

// Kill a process by PID.
void killProcessByPID() {
    std::cout << BOLD << "Enter PID to kill: " << RESET;
    std::string pidInput;
    std::getline(std::cin, pidInput);
    try {
        DWORD pid = std::stoul(pidInput);
        HANDLE hProc = OpenProcess(PROCESS_TERMINATE, FALSE, pid);
        if (!hProc) {
            std::cout << RED << BOLD << "Unable to open process with PID " << pid << RESET << std::endl;
            return;
        }
        if (TerminateProcess(hProc, 1))
            std::cout << GREEN << BOLD << "Process with PID " << pid << " killed successfully." << RESET << std::endl;
        else
            std::cout << RED << BOLD << "Failed to kill process with PID " << pid << RESET << std::endl;
        CloseHandle(hProc);
    } catch (...) {
        std::cout << RED << BOLD << "Invalid PID entered." << RESET << std::endl;
    }
}

// Change process priority (for first PID in group)
void changeProcessPriorityByIndex(const ProcessInfo &proc) {
    if (proc.pids.empty()) {
        std::cout << RED << BOLD << "No PID available for process " << proc.name << RESET << std::endl;
        return;
    }
    DWORD pid = proc.pids[0];
    HANDLE hProc = OpenProcess(PROCESS_SET_INFORMATION | PROCESS_QUERY_INFORMATION, FALSE, pid);
    if (!hProc) {
        std::cout << RED << BOLD << "Unable to open process " << pid << RESET << std::endl;
        return;
    }
    
    int priority = GetPriorityClass(hProc);
    std::cout << "Current priority for " << proc.name << " (PID " << pid << "): " << priority << std::endl;
    std::cout << "Choose new priority:\n"
              << "1: IDLE\n2: BELOW NORMAL\n3: NORMAL\n4: ABOVE NORMAL\n5: HIGH\n6: REALTIME\n"
              << "Enter choice (1-6): ";
    std::string choice;
    std::getline(std::cin, choice);
    DWORD newPriority = NORMAL_PRIORITY_CLASS;
    if (choice == "1") newPriority = IDLE_PRIORITY_CLASS;
    else if (choice == "2") newPriority = BELOW_NORMAL_PRIORITY_CLASS;
    else if (choice == "3") newPriority = NORMAL_PRIORITY_CLASS;
    else if (choice == "4") newPriority = ABOVE_NORMAL_PRIORITY_CLASS;
    else if (choice == "5") newPriority = HIGH_PRIORITY_CLASS;
    else if (choice == "6") newPriority = REALTIME_PRIORITY_CLASS;
    else {
        std::cout << YELLOW << BOLD << "Invalid choice. No changes made." << RESET << std::endl;
        CloseHandle(hProc);
        return;
    }
    
    if (SetPriorityClass(hProc, newPriority))
        std::cout << GREEN << BOLD << "Priority changed for process " << proc.name << " (PID " << pid << ")." << RESET << std::endl;
    else
        std::cout << RED << BOLD << "Failed to change priority for PID " << pid << "." << RESET << std::endl;
    
    CloseHandle(hProc);
}

// Helper: Retrieve parent process ID.
DWORD getParentProcessID(DWORD pid) {
    DWORD parentPID = 0;
    HANDLE hSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (hSnap == INVALID_HANDLE_VALUE)
        return 0;
    PROCESSENTRY32 pe32;
    pe32.dwSize = sizeof(PROCESSENTRY32);
    if (Process32First(hSnap, &pe32)) {
        do {
            if (pe32.th32ProcessID == pid) {
                parentPID = pe32.th32ParentProcessID;
                break;
            }
        } while(Process32Next(hSnap, &pe32));
    }
    CloseHandle(hSnap);
    return parentPID;
}

// Show process tree: parent and immediate children.
void showProcessTree(const ProcessInfo &proc) {
    if (proc.pids.empty()) {
        std::cout << RED << BOLD << "No PID available for process " << proc.name << RESET << std::endl;
        return;
    }
    DWORD pid = proc.pids[0];
    DWORD parentPID = getParentProcessID(pid);
    std::cout << "\n" << BOLD << UNDERLINE << "Process Tree for '" << proc.name 
              << "' (PID " << pid << "):" << RESET << std::endl;
    if (parentPID != 0)
        std::cout << "Parent PID: " << parentPID << std::endl;
    else
        std::cout << "Parent: None" << std::endl;
    
    HANDLE hSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (hSnap == INVALID_HANDLE_VALUE) {
        std::cout << RED << BOLD << "Error retrieving process snapshot." << RESET << std::endl;
        return;
    }
    PROCESSENTRY32 pe32;
    pe32.dwSize = sizeof(PROCESSENTRY32);
    std::vector<std::pair<std::string, DWORD>> children;
    if (Process32First(hSnap, &pe32)) {
        do {
            if (pe32.th32ParentProcessID == pid)
                children.push_back({pe32.szExeFile, pe32.th32ProcessID});
        } while(Process32Next(hSnap, &pe32));
    }
    CloseHandle(hSnap);
    
    if (!children.empty()) {
        std::cout << "Children:" << std::endl;
        for (auto &child : children) {
            std::cout << "  - " << child.first << " (PID " << child.second << ")" << std::endl;
        }
    } else {
        std::cout << "Children: None" << std::endl;
    }
}

// Placeholder for showing environment variables.
void showProcessEnviron(const ProcessInfo &proc) {
    std::cout << "\n" << BOLD << UNDERLINE << "Environment Variables for '" << proc.name 
              << "' (PID " << (proc.pids.empty() ? 0 : proc.pids[0]) << "):" << RESET << std::endl;
    std::cout << YELLOW << BOLD << "Feature not implemented." << RESET << std::endl;
}

// Suspend or resume a process.
void toggleSuspendResume(const ProcessInfo &proc) {
    if (proc.pids.empty()) {
        std::cout << RED << BOLD << "No PID available for process " << proc.name << RESET << std::endl;
        return;
    }
    DWORD pid = proc.pids[0];
    std::cout << "Enter 's' to suspend or 'r' to resume process " << proc.name << " (PID " << pid << "): ";
    std::string action;
    std::getline(std::cin, action);
    action = toLower(action);
    
    HANDLE hThreadSnap = CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, 0);
    if (hThreadSnap == INVALID_HANDLE_VALUE) {
        std::cout << RED << BOLD << "Error taking thread snapshot." << RESET << std::endl;
        return;
    }
    THREADENTRY32 te32;
    te32.dwSize = sizeof(THREADENTRY32);
    if (!Thread32First(hThreadSnap, &te32)) {
        std::cout << RED << BOLD << "Error reading thread snapshot." << RESET << std::endl;
        CloseHandle(hThreadSnap);
        return;
    }
    
    bool anyAction = false;
    do {
        if (te32.th32OwnerProcessID == pid) {
            HANDLE hThread = OpenThread(THREAD_SUSPEND_RESUME, FALSE, te32.th32ThreadID);
            if (hThread) {
                if (action == "s") {
                    SuspendThread(hThread);
                    anyAction = true;
                } else if (action == "r") {
                    ResumeThread(hThread);
                    anyAction = true;
                }
                CloseHandle(hThread);
            }
        }
    } while (Thread32Next(hThreadSnap, &te32));
    CloseHandle(hThreadSnap);
    
    if (anyAction) {
        if (action == "s")
            std::cout << GREEN << BOLD << "Process " << proc.name << " (PID " << pid << ") suspended." << RESET << std::endl;
        else if (action == "r")
            std::cout << GREEN << BOLD << "Process " << proc.name << " (PID " << pid << ") resumed." << RESET << std::endl;
    } else {
        std::cout << YELLOW << BOLD << "No threads modified." << RESET << std::endl;
    }
}

// List threads for a process.
void listProcessThreads(const ProcessInfo &proc) {
    if (proc.pids.empty()) {
        std::cout << RED << BOLD << "No PID available for process " << proc.name << RESET << std::endl;
        return;
    }
    DWORD pid = proc.pids[0];
    HANDLE hThreadSnap = CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, 0);
    if (hThreadSnap == INVALID_HANDLE_VALUE) {
        std::cout << RED << BOLD << "Error taking thread snapshot." << RESET << std::endl;
        return;
    }
    THREADENTRY32 te32;
    te32.dwSize = sizeof(THREADENTRY32);
    std::cout << "\n" << BOLD << UNDERLINE << "Threads for process '" << proc.name 
              << "' (PID " << pid << "):" << RESET << std::endl;
    if (Thread32First(hThreadSnap, &te32)) {
        bool found = false;
        do {
            if (te32.th32OwnerProcessID == pid) {
                std::cout << "Thread ID: " << te32.th32ThreadID << std::endl;
                found = true;
            }
        } while (Thread32Next(hThreadSnap, &te32));
        if (!found)
            std::cout << "No threads found." << std::endl;
    }
    CloseHandle(hThreadSnap);
}

// Print command menu.
void printMenu() {
    std::cout << "\n" << BOLD << CYAN
              << "Options:\n"
              << "[K] Kill by index (enter numbers, e.g. 1,3,5)\n"
              << "[S] Search processes\n"
              << "[D] Show process details\n"
              << "[P] Kill by PID\n"
              << "[N] Change process priority\n"
              << "[T] Show process tree\n"
              << "[V] Show environment variables\n"
              << "[X] Suspend/Resume a process\n"
              << "[L] List process threads\n"
              << "[E] Exit\n"
              << RESET;
}

int main() {
    while (true) {
        std::cout << "\n" << std::string(80, '=') << std::endl;
        std::cout << BOLD << CYAN << "Process Monitor" << RESET << std::endl;
        
        auto processes = getWindowsProcesses();
        auto sortedProcesses = displayProcesses(processes);
        displaySystemOverview();
        printMenu();
        std::cout << BOLD << "Enter option: " << RESET;
        std::string command;
        std::getline(std::cin, command);
        command = toLower(command);
        
        if (command == "e") {
            std::cout << GREEN << BOLD << "Exiting..." << RESET << std::endl;
            break;
        }
        else if (command == "s") {
            std::cout << BOLD << "Enter search term: " << RESET;
            std::string term;
            std::getline(std::cin, term);
            if (term.empty()) {
                std::cout << YELLOW << BOLD << "No search term entered. Returning to main menu." << RESET << std::endl;
                continue;
            }
            auto filtered = searchProcesses(sortedProcesses, term);
            if (filtered.empty()) {
                std::cout << YELLOW << BOLD << "No processes matching '" << term << "' found." << RESET << std::endl;
                continue;
            }
            std::cout << "\n" << CYAN << BOLD << "Search results for '" << term << "':" << RESET << std::endl;
            auto filteredSorted = displayProcesses(filtered);
            displaySystemOverview();
            killProcessesByImage(filteredSorted);
        }
        else if (command == "d") {
            std::cout << BOLD << "Enter the process number for details: " << RESET;
            std::string num;
            std::getline(std::cin, num);
            try {
                int idx = std::stoi(num) - 1;
                if (idx < 0 || idx >= static_cast<int>(sortedProcesses.size())) {
                    std::cout << RED << BOLD << "Index " << num << " out of range." << RESET << std::endl;
                    continue;
                }
                showProcessDetails(sortedProcesses[idx]);
            } catch (...) {
                std::cout << RED << BOLD << "Invalid input. Please enter a valid number." << RESET << std::endl;
            }
        }
        else if (command == "p") {
            killProcessByPID();
        }
        else if (command == "n") {
            std::cout << BOLD << "Enter the process number to change priority: " << RESET;
            std::string num;
            std::getline(std::cin, num);
            try {
                int idx = std::stoi(num) - 1;
                if (idx < 0 || idx >= static_cast<int>(sortedProcesses.size())) {
                    std::cout << RED << BOLD << "Index " << num << " out of range." << RESET << std::endl;
                    continue;
                }
                changeProcessPriorityByIndex(sortedProcesses[idx]);
            } catch (...) {
                std::cout << RED << BOLD << "Invalid input. Please enter a valid number." << RESET << std::endl;
            }
        }
        else if (command == "t") {
            std::cout << BOLD << "Enter the process number for tree view: " << RESET;
            std::string num;
            std::getline(std::cin, num);
            try {
                int idx = std::stoi(num) - 1;
                if (idx < 0 || idx >= static_cast<int>(sortedProcesses.size())) {
                    std::cout << RED << BOLD << "Index " << num << " out of range." << RESET << std::endl;
                    continue;
                }
                showProcessTree(sortedProcesses[idx]);
            } catch (...) {
                std::cout << RED << BOLD << "Invalid input. Please enter a valid number." << RESET << std::endl;
            }
        }
        else if (command == "v") {
            std::cout << BOLD << "Enter the process number to show environment variables: " << RESET;
            std::string num;
            std::getline(std::cin, num);
            try {
                int idx = std::stoi(num) - 1;
                if (idx < 0 || idx >= static_cast<int>(sortedProcesses.size())) {
                    std::cout << RED << BOLD << "Index " << num << " out of range." << RESET << std::endl;
                    continue;
                }
                showProcessEnviron(sortedProcesses[idx]);
            } catch (...) {
                std::cout << RED << BOLD << "Invalid input. Please enter a valid number." << RESET << std::endl;
            }
        }
        else if (command == "x") {
            std::cout << BOLD << "Enter the process number to suspend/resume: " << RESET;
            std::string num;
            std::getline(std::cin, num);
            try {
                int idx = std::stoi(num) - 1;
                if (idx < 0 || idx >= static_cast<int>(sortedProcesses.size())) {
                    std::cout << RED << BOLD << "Index " << num << " out of range." << RESET << std::endl;
                    continue;
                }
                toggleSuspendResume(sortedProcesses[idx]);
            } catch (...) {
                std::cout << RED << BOLD << "Invalid input. Please enter a valid number." << RESET << std::endl;
            }
        }
        else if (command == "l") {
            std::cout << BOLD << "Enter the process number to list threads: " << RESET;
            std::string num;
            std::getline(std::cin, num);
            try {
                int idx = std::stoi(num) - 1;
                if (idx < 0 || idx >= static_cast<int>(sortedProcesses.size())) {
                    std::cout << RED << BOLD << "Index " << num << " out of range." << RESET << std::endl;
                    continue;
                }
                listProcessThreads(sortedProcesses[idx]);
            } catch (...) {
                std::cout << RED << BOLD << "Invalid input. Please enter a valid number." << RESET << std::endl;
            }
        }
        // If the command appears to be numbers (e.g., "1,3,5")
        else if (!command.empty() && (std::isdigit(command[0]) || command.find(',') != std::string::npos)) {
            killProcessesByImage(sortedProcesses);
        }
        else {
            std::cout << YELLOW << BOLD << "Unknown command. Please try again." << RESET << std::endl;
        }
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
    
    return 0;
}
