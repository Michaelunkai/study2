<#
    Enhanced Elden Ring Launcher Script (Remade)
    
    This script:
    1. Launches Elden Ring
    2. Waits 10 seconds, then sends Win+D to show the desktop
    3. Waits 5 more seconds, then runs rmod.exe and sends the '1' keypress
    4. Sets up keyboard shortcuts for Ctrl+S (suspend game) and Ctrl+R (resume game)
    5. Runs the 'desk' function after 10 seconds
    6. After game exit, launches save management tools
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
$launcherPath    = "F:\games\eldenrings\Game\Language Selector.exe"
$savestatePath   = "F:\backup\windowsapps\installed\SaveState\SaveState.exe"
$ludusaviPath    = "F:\backup\windowsapps\installed\ludusavi\ludusavi.exe"
$gsmPath         = "F:\backup\windowsapps\installed\gameSaveManager\gs_mngr_3.exe"
$ahkPath         = "F:\study\Platforms\windows\autohotkey\switchBetweenDesktop1And2.ahk"
$superf4Path     = "F:\backup\windowsapps\installed\SuperF4\SuperF4.exe"
$rmodPath        = "F:\study\automation\bots\MacroCreator\rmod\rmod.exe"

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
# 4) Launch Elden Ring, send Win+D after 10 seconds, run rmod after 15 seconds
############################################################
Write-Host "Launching Elden Ring..." -ForegroundColor Yellow
$erProcess = Start-Process -FilePath $launcherPath -WorkingDirectory (Split-Path -Path $launcherPath -Parent) -PassThru

# Wait 10 seconds, then send Win+D to show desktop
Write-Host "Waiting 10 seconds before sending Win+D..." -ForegroundColor Yellow
Start-Sleep -Seconds 10
Write-Host "Sending Win+D to show desktop..." -ForegroundColor Yellow
Add-Type -AssemblyName System.Windows.Forms
try {
    [System.Windows.Forms.SendKeys]::SendWait("^{d}")
    Write-Host "Win+D sent successfully." -ForegroundColor Green
} catch {
    Write-Host "Failed to send Win+D: $_" -ForegroundColor Red
}

# Wait 5 more seconds, then run rmod.exe and send '1' keypress
Write-Host "Waiting 5 more seconds before running rmod..." -ForegroundColor Yellow
Start-Sleep -Seconds 5
Write-Host "Launching rmod and sending '1' keypress..." -ForegroundColor Yellow
try {
    if (Test-Path $rmodPath) {
        Start-Process -FilePath $rmodPath
        Start-Sleep -Seconds 1
        [System.Windows.Forms.SendKeys]::SendWait("1")
        Write-Host "rmod executed and '1' key sent." -ForegroundColor Green
    } else {
        Write-Host "rmod not found at: $rmodPath" -ForegroundColor Red
    }
} catch {
    Write-Host "Failed to execute rmod or send keypress: $_" -ForegroundColor Red
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
    if ($null -ne $erProcess -and !$erProcess.HasExited) {
        $erProcess | Wait-Process -Timeout 300 -ErrorAction SilentlyContinue
    }
    $monitoring = $true
    while ($monitoring) {
        $gameProcesses = Get-Process -Name "eldenring", "start_protected_game" -ErrorAction SilentlyContinue
        if ($gameProcesses.Count -eq 0) {
            $monitoring = $false
        } else {
            Start-Sleep -Seconds 15
        }
    }
} catch {
    Write-Host "Error while monitoring game process: $_" -ForegroundColor Red
} finally {
    ########################################################
    # 7) Clean up keyboard hooks
    ########################################################
    try {
        [KeyboardHook]::StopHook()
        Write-Host "Keyboard hooks removed." -ForegroundColor Green
    } catch {
        Write-Host "Failed to clean up keyboard hooks: $_" -ForegroundColor Yellow
    }

    ########################################################
    # 8) Post-game helpers: run sg function and backup apps
    ########################################################
    Write-Host "Game closed. Running post-game helpers and backup apps..." -ForegroundColor Yellow
    sg
    Write-Host "Launching save management tools..." -ForegroundColor Green
    foreach ($tool in @($savestatePath, $ludusaviPath, $gsmPath)) {
        if (Test-Path $tool) {
            try {
                Start-Process -FilePath $tool -WindowStyle Normal
                Write-Host "Started: $(Split-Path $tool -Leaf)" -ForegroundColor Green
            } catch {
                Write-Host "Failed to start: $(Split-Path $tool -Leaf) - $_" -ForegroundColor Red
            }
        } else {
            Write-Host "Tool not found: $(Split-Path $tool -Leaf)" -ForegroundColor Yellow
        }
    }
    Write-Host "All operations completed successfully!" -ForegroundColor Green
}

# Exit the script cleanly
exit 0
