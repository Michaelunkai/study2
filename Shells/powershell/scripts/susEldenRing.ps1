Add-Type -TypeDefinition @"
using System;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Windows.Forms;
using System.Text;
using System.IO;
using System.Threading;

public class SuspendResumeHook {
    private const int WH_KEYBOARD_LL = 13;
    private const int WM_KEYDOWN = 0x0100;
    private const int WM_KEYUP = 0x0101;
    private static IntPtr hookId = IntPtr.Zero;
    private static HookProc hookProc;
    private static bool ctrlDown = false;
    private static bool isProcessing = false;
    private static readonly string psSuspendPath = @"F:\backup\windowsapps\installed\PSTools\pssuspend.exe";
    private static readonly object lockObject = new object();

    public delegate IntPtr HookProc(int nCode, IntPtr wParam, IntPtr lParam);

    [DllImport("user32.dll", SetLastError = true)]
    public static extern IntPtr SetWindowsHookEx(int idHook, HookProc lpfn, IntPtr hMod, uint dwThreadId);

    [DllImport("user32.dll", SetLastError = true)]
    public static extern bool UnhookWindowsHookEx(IntPtr hhk);

    [DllImport("user32.dll")]
    public static extern IntPtr CallNextHookEx(IntPtr hhk, int nCode, IntPtr wParam, IntPtr lParam);

    [DllImport("kernel32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    public static extern IntPtr GetModuleHandle(string lpModuleName);

    [DllImport("user32.dll")]
    public static extern short GetAsyncKeyState(Keys vKey);

    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();

    [DllImport("user32.dll", SetLastError = true)]
    public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint processId);

    [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    public static extern int GetWindowText(IntPtr hWnd, StringBuilder text, int count);

    public static void Start() {
                if (!System.IO.File.Exists(psSuspendPath)) {
            throw new FileNotFoundException("PSTools pssuspend.exe not found at " + psSuspendPath);
        }
        
        hookProc = new HookProc(KeyboardCallback);
        hookId = SetHook(hookProc);
        
        if (hookId == IntPtr.Zero) {
            throw new Exception("Failed to set keyboard hook. Error code: " + Marshal.GetLastWin32Error());
        }
    }

    public static void Stop() {
        if (hookId != IntPtr.Zero) {
            UnhookWindowsHookEx(hookId);
            hookId = IntPtr.Zero;
        }
    }

    private static IntPtr SetHook(HookProc proc) {
        using (Process curProcess = Process.GetCurrentProcess())
        using (ProcessModule curModule = curProcess.MainModule) {
            return SetWindowsHookEx(WH_KEYBOARD_LL, proc, GetModuleHandle(curModule.ModuleName), 0);
        }
    }

    private static IntPtr KeyboardCallback(int nCode, IntPtr wParam, IntPtr lParam) {
        if (nCode >= 0 && !isProcessing) {
            int keyCode = Marshal.ReadInt32(lParam);

            if (wParam == (IntPtr)WM_KEYDOWN) {
                if (keyCode == (int)Keys.ControlKey || keyCode == (int)Keys.LControlKey || keyCode == (int)Keys.RControlKey) {
                    ctrlDown = true;
                } else if (ctrlDown && keyCode == (int)Keys.S) {
                    ThreadPool.QueueUserWorkItem(new WaitCallback((_) => {
                        lock (lockObject) {
                            try {
                                isProcessing = true;
                                SuspendActiveProcess();
                            } catch (Exception ex) {
                                Console.WriteLine("Error suspending process: " + ex.Message);
                            } finally {
                                isProcessing = false;
                            }
                        }
                    }));
                    return (IntPtr)1;                 } else if (ctrlDown && keyCode == (int)Keys.R) {
                    ThreadPool.QueueUserWorkItem(new WaitCallback((_) => {
                        lock (lockObject) {
                            try {
                                isProcessing = true;
                                ResumeActiveProcess();
                            } catch (Exception ex) {
                                Console.WriteLine("Error resuming process: " + ex.Message);
                            } finally {
                                isProcessing = false;
                            }
                        }
                    }));
                    return (IntPtr)1;                 }
            } else if (wParam == (IntPtr)WM_KEYUP) {
                if (keyCode == (int)Keys.ControlKey || keyCode == (int)Keys.LControlKey || keyCode == (int)Keys.RControlKey) {
                    ctrlDown = false;
                }
            }
        }
        return CallNextHookEx(hookId, nCode, wParam, lParam);
    }

    private static Process GetActiveProcess() {
        try {
            IntPtr hwnd = GetForegroundWindow();
            if (hwnd == IntPtr.Zero) {
                Console.WriteLine("No active window found");
                return null;
            }
            
            uint processId;
            GetWindowThreadProcessId(hwnd, out processId);
            if (processId == 0) {
                Console.WriteLine("Could not get process ID for active window");
                return null;
            }

            StringBuilder windowTitle = new StringBuilder(256);
            GetWindowText(hwnd, windowTitle, 256);

            Process process = Process.GetProcessById((int)processId);
            Console.WriteLine("Active window: " + windowTitle + ", Process: " + process.ProcessName + " (ID: " + processId + ")");

            return process;
        } catch (Exception e) {
            Console.WriteLine("Error getting active process: " + e.Message);
            return null;
        }
    }

    private static void SuspendActiveProcess() {
        Process activeProcess = GetActiveProcess();
        if (activeProcess != null && !String.IsNullOrEmpty(activeProcess.ProcessName)) {
            string processName = activeProcess.ProcessName;
            Console.WriteLine("Suspending process: " + processName);
            RunPsSuspendCommand(processName, false);
        }
    }

    private static void ResumeActiveProcess() {
        Process activeProcess = GetActiveProcess();
        if (activeProcess != null && !String.IsNullOrEmpty(activeProcess.ProcessName)) {
            string processName = activeProcess.ProcessName;
            Console.WriteLine("Resuming process: " + processName);
            RunPsSuspendCommand(processName, true);
        }
    }

    private static void RunPsSuspendCommand(string processName, bool resume) {
        try {
            ProcessStartInfo psi = new ProcessStartInfo();
            psi.FileName = psSuspendPath;
            psi.Arguments = (resume ? "-r " : "") + processName + ".exe";
            psi.CreateNoWindow = true;
            psi.UseShellExecute = false;
            psi.RedirectStandardOutput = true;
            psi.RedirectStandardError = true;

            using (Process process = Process.Start(psi)) {
                process.WaitForExit(5000);                 string output = process.StandardOutput.ReadToEnd();
                string error = process.StandardError.ReadToEnd();
                
                if (!String.IsNullOrEmpty(error)) {
                    Console.WriteLine("Error from PSSuspend: " + error);
                }
                if (!String.IsNullOrEmpty(output)) {
                    Console.WriteLine("Output from PSSuspend: " + output);
                }
                
                if (!process.HasExited) {
                    process.Kill();
                    Console.WriteLine("PSSuspend process was terminated due to timeout");
                }
            }
        } catch (Exception e) {
            Console.WriteLine("PSSuspend command error: " + e.Message);
        }
    }
}
"@ -ReferencedAssemblies System.Windows.Forms, System.Runtime.InteropServices

# Clear error variable
$Error.Clear()

# Path to pssuspend.exe
$psSuspendPath = "F:\backup\windowsapps\installed\PSTools\pssuspend.exe"

# Check if pssuspend.exe exists
if (-not (Test-Path $psSuspendPath)) {
    Write-Host "Error: pssuspend.exe not found at $psSuspendPath" -ForegroundColor Red
    Write-Host "Please make sure PSTools is installed and the path is correct." -ForegroundColor Yellow
    exit 1
}

try {
    # Stop any existing hooks before starting
    try {
        [SuspendResumeHook]::Stop()
        Write-Host "Previous hooks stopped successfully" -ForegroundColor Green
    } catch {
        # No previous hooks or failed to stop them
        Write-Host "No previous hooks found or failed to stop them: $($_.Exception.Message)" -ForegroundColor Yellow
    }

    # Start new hook
    [SuspendResumeHook]::Start()
    Write-Host "Hotkeys registered successfully:" -ForegroundColor Green
    Write-Host "  → Ctrl+S to suspend the currently active application" -ForegroundColor Cyan
    Write-Host "  → Ctrl+R to resume the currently active application" -ForegroundColor Cyan
    Write-Host "Script will continue running until PowerShell session is closed." -ForegroundColor Yellow
    
    # Keep the script running with more responsive checks
    while ($true) {
        # Check if hook is still active
        try {
            if ([SuspendResumeHook]::hookId -eq [IntPtr]::Zero) {
                Write-Host "Warning: Hook was deactivated. Attempting to restart..." -ForegroundColor Yellow
                [SuspendResumeHook]::Start()
            }
        } catch {
            Write-Host "Error checking hook status: $($_.Exception.Message)" -ForegroundColor Yellow
            # Try to restart the hook
            try {
                [SuspendResumeHook]::Start()
            } catch {
                Write-Host "Failed to restart hook: $($_.Exception.Message)" -ForegroundColor Red
            }
        }
        
        Start-Sleep -Seconds 5
    }
} catch {
    Write-Host "Critical error in suspend    Write-Host "Stack trace: $($_.Exception.StackTrace)" -ForegroundColor Red
    exit 1
}
}
