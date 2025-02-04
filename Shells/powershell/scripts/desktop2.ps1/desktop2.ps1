Add-Type @"
    using System;
    using System.Runtime.InteropServices;
    
    public class VirtualDesktop {
        [DllImport("user32.dll")]
        public static extern IntPtr GetForegroundWindow();

        [DllImport("user32.dll")]
        public static extern bool EnumWindows(EnumWindowsProc enumProc, IntPtr lParam);
        
        public delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lParam);
        
        [DllImport("user32.dll")]
        public static extern bool IsWindowVisible(IntPtr hWnd);
        
        [DllImport("user32.dll", SetLastError = true)]
        public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint lpdwProcessId);

        [DllImport("user32.dll", CharSet = CharSet.Unicode)]
        public static extern int GetWindowText(IntPtr hWnd, System.Text.StringBuilder text, int count);
    }
"@

# Get all visible windows
$windows = New-Object System.Collections.ArrayList

$enumWindows = [VirtualDesktop+EnumWindowsProc] {
    param([IntPtr]$hWnd, [IntPtr]$lParam)
    
    if ([VirtualDesktop]::IsWindowVisible($hWnd)) {
        $processId = 0
        [VirtualDesktop]::GetWindowThreadProcessId($hWnd, [ref]$processId)
        
        $title = New-Object System.Text.StringBuilder(256)
        [VirtualDesktop]::GetWindowText($hWnd, $title, 256)
        
        if ($title.Length -gt 0 -and $processId -gt 0) {
            $null = $windows.Add(@{
                Handle = $hWnd
                Title = $title.ToString()
                ProcessId = $processId
            })
        }
    }
    return $true
}

[VirtualDesktop]::EnumWindows($enumWindows, [IntPtr]::Zero)

# Send Windows+Ctrl+Right to move to desktop 2
$wshell = New-Object -ComObject wscript.shell
$wshell.SendKeys('^%{RIGHT}')
Start-Sleep -Milliseconds 500

# Activate each window to bring it to the current desktop
foreach ($window in $windows) {
    try {
        $process = Get-Process -Id $window.ProcessId -ErrorAction SilentlyContinue
        if ($process) {
            $wshell.AppActivate($window.Title)
            Start-Sleep -Milliseconds 100
        }
    } catch {
        Write-Warning "Could not move window: $_"
    }
}

Write-Host "Operation completed. Please check if windows were moved successfully."
