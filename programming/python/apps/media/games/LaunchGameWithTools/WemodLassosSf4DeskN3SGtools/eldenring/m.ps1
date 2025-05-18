<#
    Enhanced Elden Ring Launcher Script (Remade)
    
    This script:
    1. Launches custom runERandWemod.exe and sends '1' keypress
    2. Sets up keyboard shortcuts for Ctrl+S (suspend game) and Ctrl+R (resume game)
    3. Runs the 'desk' function after 10 seconds
    4. After game exit, launches backup executable and sends '1' keypress
#>

############################################################
# 1) User-defined helper functions
############################################################
function desk {
    Write-Host "Running desk function - switching between desktop 1 and 2..." -ForegroundColor Cyan
    if (Test-Path $ahkPath) {
        Push-Location -Path (Split-Path -Path $ahkPath -Parent)
        try {
            & $ahkPath
            Write-Host "Desktop switch executed." -ForegroundColor Green
        } catch {
            Write-Host "Error running AHK script: $_" -ForegroundColor Red
        }
        Pop-Location
    } else {
        Write-Host "AHK script not found at: $ahkPath" -ForegroundColor Red
    }
}

function superf4 {
    Write-Host "Running superf4 function - starting SuperF4..." -ForegroundColor Cyan
    $exeWD = Split-Path -Path $superf4Path -Parent
    if (Test-Path $superf4Path) {
        try {
            Start-Process -FilePath $superf4Path -WorkingDirectory $exeWD
            Write-Host "SuperF4 started." -ForegroundColor Green
        } catch {
            Write-Host "Failed to start SuperF4: $_" -ForegroundColor Red
        }
    } else {
        Write-Host "SuperF4 not found at: $superf4Path" -ForegroundColor Red
    }
}

function sg {
    Write-Host "Running sg function..." -ForegroundColor Cyan
    # Add your sg function implementation here if needed
}

function rr {
    Write-Host "Running rr function sequence..." -ForegroundColor Green
    desk
    superf4
}

function sused {
    Write-Host "Suspending Elden Ring process..." -ForegroundColor Yellow
    try {
        & "F:\backup\windowsapps\installed\PSTools\pssuspend.exe" eldenring.exe
        Write-Host "Elden Ring suspended." -ForegroundColor Green
    } catch {
        Write-Host "Failed to suspend Elden Ring: $_" -ForegroundColor Red
    }
}

function resed {
    Write-Host "Resuming Elden Ring process..." -ForegroundColor Yellow
    try {
        & "F:\backup\windowsapps\installed\PSTools\pssuspend.exe" -r eldenring.exe
        Write-Host "Elden Ring resumed." -ForegroundColor Green
    } catch {
        Write-Host "Failed to resume Elden Ring: $_" -ForegroundColor Red
    }
}

############################################################
# 2) Path configuration - Edit these paths as needed
############################################################
$gamePath        = "F:\games\eldenrings\Game\eldenring.exe"
$launcherPath    = "F:\study\programming\python\apps\media\games\LaunchGameWithTools\WemodLassosSf4DeskN3SGtools\eldenring\runERandWemod.exe"
$ahkPath         = "F:\study\Platforms\windows\autohotkey\switchBetweenDesktop1And2.ahk"
$superf4Path     = "F:\backup\windowsapps\installed\SuperF4\SuperF4.exe"
$backupPath      = "F:\study\programming\python\apps\media\games\LaunchGameWithTools\WemodLassosSf4DeskN3SGtools\eldenring\backupeldenring.exe"

############################################################
# 3) Setup keyboard shortcuts
############################################################
Add-Type -TypeDefinition @"
using System;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Windows.Forms;

public class KeyboardHook {
    private const int WH_KEYBOARD_LL = 13;
    private const int WM_KEYDOWN = 0x0100;
    private static IntPtr hookId = IntPtr.Zero;
    private static HookProc hookProc;
    private static bool ctrlPressed = false;

    public delegate IntPtr HookProc(int nCode, IntPtr wParam, IntPtr lParam);

    [DllImport("user32.dll")]
    public static extern IntPtr SetWindowsHookEx(int idHook, HookProc lpfn, IntPtr hMod, uint dwThreadId);

    [DllImport("user32.dll")]
    public static extern bool UnhookWindowsHookEx(IntPtr hhk);

    [DllImport("user32.dll")]
    public static extern IntPtr CallNextHookEx(IntPtr hhk, int nCode, IntPtr wParam, IntPtr lParam);

    [DllImport("kernel32.dll")]
    public static extern IntPtr GetModuleHandle(string lpModuleName);

    [DllImport("user32.dll")]
    public static extern short GetAsyncKeyState(Keys vKey);

    public static void StartHook() {
        hookProc = new HookProc(HookCallback);
        hookId = SetHook(hookProc);
    }

    public static void StopHook() {
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

    private static IntPtr HookCallback(int nCode, IntPtr wParam, IntPtr lParam) {
        if (nCode >= 0 && wParam == (IntPtr)WM_KEYDOWN) {
            int vkCode = Marshal.ReadInt32(lParam);
            if (vkCode == (int)Keys.ControlKey || vkCode == (int)Keys.LControlKey || vkCode == (int)Keys.RControlKey) {
                ctrlPressed = true;
            }
            else if (ctrlPressed && vkCode == (int)Keys.S) {
                RunPowerShellCommand("sused");
                return (IntPtr)1;
            }
            else if (ctrlPressed && vkCode == (int)Keys.R) {
                RunPowerShellCommand("resed");
                return (IntPtr)1;
            }
            else {
                ctrlPressed = (GetAsyncKeyState(Keys.ControlKey) & 0x8000) != 0;
            }
        }
        return CallNextHookEx(hookId, nCode, wParam, lParam);
    }

    private static void RunPowerShellCommand(string command) {
        try {
            ProcessStartInfo psi = new ProcessStartInfo();
            psi.FileName = "powershell.exe";
            psi.Arguments = "-Command \"" + command + "\"";
            psi.CreateNoWindow = true;
            psi.UseShellExecute = false;
            Process.Start(psi);
        }
        catch (Exception ex) {
            Console.WriteLine("Error running command: " + ex.Message);
        }
    }
}
"@ -ReferencedAssemblies System.Windows.Forms, System.Runtime.InteropServices

Write-Host "Setting up keyboard shortcuts..." -ForegroundColor Cyan
try {
    [KeyboardHook]::StartHook()
    Write-Host "Keyboard shortcuts registered successfully." -ForegroundColor Green
    Write-Host "Use Ctrl+S to suspend Elden Ring and Ctrl+R to resume." -ForegroundColor Green
} catch {
    Write-Host "Failed to register keyboard shortcuts: $_" -ForegroundColor Red
    Write-Host "The suspend/resume features will need to be called manually." -ForegroundColor Yellow
}

############################################################
# 4) Launch runERandWemod.exe and press 1
############################################################
Write-Host "Launching runERandWemod.exe..." -ForegroundColor Yellow
try {
    Start-Process -FilePath $launcherPath -WorkingDirectory (Split-Path -Path $launcherPath -Parent)
    Write-Host "runERandWemod.exe started, waiting 1 second..." -ForegroundColor Green
    Start-Sleep -Seconds 1
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.SendKeys]::SendWait("1")
    Write-Host "Key '1' sent to runERandWemod.exe." -ForegroundColor Green
} catch {
    Write-Host "Failed to start runERandWemod.exe or send keypress: $_" -ForegroundColor Red
}

############################################################
# 5) Wait 10 seconds, then run pre-game helpers (rr)
############################################################
Write-Host "Waiting 10 seconds before running pre-game helpers..." -ForegroundColor Yellow
Start-Sleep -Seconds 10
Write-Host "Running pre-game helper functions..." -ForegroundColor Yellow
rr

############################################################
# 6) Wait for main game process to exit
############################################################
Write-Host "Monitoring for game exit..." -ForegroundColor Yellow
try {
    $monitoring = $true
    $checkCounter = 0
    
    while ($monitoring) {
        $gameProcesses = Get-Process -Name "eldenring", "start_protected_game" -ErrorAction SilentlyContinue
        
        if ($gameProcesses.Count -eq 0) {
            # Game has exited
            Write-Host "Game processes detected as closed. Confirming..." -ForegroundColor Green
            $monitoring = $false
        } else {
            # Only show status message every 30 checks (30 seconds) to avoid log spam
            $checkCounter++
            if ($checkCounter % 30 -eq 0) {
                Write-Host "Game still running. Continuing to monitor..." -ForegroundColor Yellow
            }
            # Check much more frequently - every 1 second
            Start-Sleep -Seconds 1
        }
    }
    
    # Quick double-check to ensure game is truly closed
    Start-Sleep -Milliseconds 500
    $finalCheck = Get-Process -Name "eldenring", "start_protected_game" -ErrorAction SilentlyContinue
    if ($finalCheck.Count -gt 0) {
        Write-Host "Additional game processes detected. Waiting for complete closure..." -ForegroundColor Yellow
        while ($finalCheck.Count -gt 0) {
            Start-Sleep -Milliseconds 500
            $finalCheck = Get-Process -Name "eldenring", "start_protected_game" -ErrorAction SilentlyContinue
        }
    }
    
    # Now it's confirmed that the game is closed
    Write-Host "Game processes confirmed closed - running sg function..." -ForegroundColor Cyan
    sg
} catch {
    Write-Host "Error while monitoring game process: $_" -ForegroundColor Red
}

############################################################
# 7) Clean up keyboard hooks and run backup
############################################################
try {
    # Clean up keyboard hooks
    [KeyboardHook]::StopHook()
    Write-Host "Keyboard hooks removed." -ForegroundColor Green
    
    # Run backup executable and press 1
    Write-Host "Now running backup executable..." -ForegroundColor Yellow
    if (Test-Path $backupPath) {
        try {
            Start-Process -FilePath $backupPath
            Write-Host "Backup executable started, waiting 1 second..." -ForegroundColor Green
            Start-Sleep -Seconds 1
            [System.Windows.Forms.SendKeys]::SendWait("1")
            Write-Host "Key '1' sent to backup executable." -ForegroundColor Green
        } catch {
            Write-Host "Failed to start backup executable or send keypress: $_" -ForegroundColor Red
        }
    } else {
        Write-Host "Backup executable not found at: $backupPath" -ForegroundColor Red
    }
    
    Write-Host "All operations completed successfully!" -ForegroundColor Green
} catch {
    Write-Host "Error during cleanup or backup: $_" -ForegroundColor Red
}

# Exit the script cleanly
exit 0
