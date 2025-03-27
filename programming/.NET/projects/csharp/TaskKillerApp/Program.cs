using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;

class ProcessInfo {
    public string ImageName { get; set; }
    public int PID { get; set; }
}

class Program {
    static void Main(string[] args) {
        // Retrieve the list of Windows processes via tasklist.exe
        List<ProcessInfo> processes = GetWindowsProcesses();
        if (processes.Count == 0) {
            Console.WriteLine("No processes found.");
            return;
        }

        Console.WriteLine("List of Windows processes:");
        for (int i = 0; i < processes.Count; i++) {
            Console.WriteLine($"{i + 1}. {processes[i].ImageName} (PID: {processes[i].PID})");
        }
        
        Console.WriteLine("\nEnter the number(s) of the process to force close (comma-separated):");
        string input = Console.ReadLine();
        string[] selections = input.Split(',', StringSplitOptions.RemoveEmptyEntries);
        foreach (var sel in selections) {
            if (int.TryParse(sel.Trim(), out int index)) {
                if (index >= 1 && index <= processes.Count) {
                    int pid = processes[index - 1].PID;
                    ForceKillProcess(pid);
                } else {
                    Console.WriteLine($"Invalid selection: {index}");
                }
            } else {
                Console.WriteLine($"Invalid input: {sel}");
            }
        }
    }

    static List<ProcessInfo> GetWindowsProcesses() {
        List<ProcessInfo> list = new List<ProcessInfo>();
        try {
            ProcessStartInfo psi = new ProcessStartInfo {
                FileName = "tasklist.exe",
                Arguments = "/fo csv /nh", // CSV format, no header
                RedirectStandardOutput = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            using (Process proc = Process.Start(psi))
            using (StreamReader sr = proc.StandardOutput)
            {
                string output = sr.ReadToEnd();
                proc.WaitForExit();
                using (StringReader reader = new StringReader(output)) {
                    string line;
                    while ((line = reader.ReadLine()) != null) {
                        string[] parts = ParseCsvLine(line);
                        if (parts.Length >= 2 && int.TryParse(parts[1], out int pid)) {
                            list.Add(new ProcessInfo { ImageName = parts[0], PID = pid });
                        }
                    }
                }
            }
        }
        catch (Exception ex) {
            Console.WriteLine("Error retrieving processes: " + ex.Message);
        }
        return list;
    }

    // Simple CSV parser that handles quoted fields
    static string[] ParseCsvLine(string line) {
        List<string> result = new List<string>();
        bool inQuotes = false;
        string current = "";
        foreach (char c in line) {
            if (c == '\"') {
                inQuotes = !inQuotes;
            } else if (c == ',' && !inQuotes) {
                result.Add(current);
                current = "";
            } else {
                current += c;
            }
        }
        result.Add(current);
        // Trim spaces and quotes from each field
        for (int i = 0; i < result.Count; i++) {
            result[i] = result[i].Trim(' ', '\"');
        }
        return result.ToArray();
    }

    static void ForceKillProcess(int pid) {
        try {
            ProcessStartInfo psi = new ProcessStartInfo {
                FileName = "taskkill.exe",
                Arguments = $"/PID {pid} /F",
                RedirectStandardOutput = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };
            using (Process proc = Process.Start(psi))
            using (StreamReader sr = proc.StandardOutput) {
                string output = sr.ReadToEnd();
                proc.WaitForExit();
                Console.WriteLine($"Terminated process with PID {pid}. Output: {output}");
            }
        }
        catch (Exception ex) {
            Console.WriteLine($"Error killing process {pid}: {ex.Message}");
        }
    }
}
