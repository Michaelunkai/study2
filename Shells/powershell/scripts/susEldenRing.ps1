Add-Type -TypeDefinition @"
using System;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Windows.Forms;

public class SuspendResumeHook {
    private const int WH_KEYBOARD_LL = 13;
    private const int WM_KEYDOWN = 0x0100;
    private static IntPtr hookId = IntPtr.Zero;
    private static HookProc hookProc;
    private static bool ctrlDown = false;

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

    public static void Start() {
        hookProc = new HookProc(Callback);
        hookId = SetHook(hookProc);
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

    private static IntPtr Callback(int nCode, IntPtr wParam, IntPtr lParam) {
        if (nCode >= 0 && wParam == (IntPtr)WM_KEYDOWN) {
            int keyCode = Marshal.ReadInt32(lParam);
            if (keyCode == (int)Keys.ControlKey || keyCode == (int)Keys.LControlKey || keyCode == (int)Keys.RControlKey) {
                ctrlDown = true;
            } else if (ctrlDown && keyCode == (int)Keys.S) {
                RunCommand("F:\\backup\\windowsapps\\installed\\PSTools\\pssuspend.exe eldenring.exe");
                return (IntPtr)1;
            } else if (ctrlDown && keyCode == (int)Keys.R) {
                RunCommand("F:\\backup\\windowsapps\\installed\\PSTools\\pssuspend.exe -r eldenring.exe");
                return (IntPtr)1;
            } else {
                ctrlDown = (GetAsyncKeyState(Keys.ControlKey) & 0x8000) != 0;
            }
        }
        return CallNextHookEx(hookId, nCode, wParam, lParam);
    }

    private static void RunCommand(string command) {
        try {
            ProcessStartInfo psi = new ProcessStartInfo("powershell.exe", "-Command \"" + command + "\"");
            psi.CreateNoWindow = true;
            psi.UseShellExecute = false;
            Process.Start(psi);
        } catch (Exception e) {
            Console.WriteLine("Command error: " + e.Message);
        }
    }
}
"@ -ReferencedAssemblies System.Windows.Forms, System.Runtime.InteropServices

try {
    [SuspendResumeHook]::Start()
    Write-Host "Hotkeys registered: Ctrl+S to suspend, Ctrl+R to resume Elden Ring" -ForegroundColor Green
} catch {
    Write-Host "Failed to register suspend/resume hotkeys: $_" -ForegroundColor Red
}
