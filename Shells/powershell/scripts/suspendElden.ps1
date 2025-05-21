Add-Type @" 
using System; 
using System.Runtime.InteropServices; 
public class Win {
    [DllImport("user32.dll")] public static extern bool ShowWindowAsync(IntPtr hWnd, int nCmdShow); 
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd); 
}
"@; $hwnd = (Get-Process eldenring).MainWindowHandle; [Win]::ShowWindowAsync($hwnd, 1); [Win]::SetForegroundWindow($hwnd); Start-Sleep -Milliseconds 500; (New-Object -ComObject WScript.Shell).SendKeys('^s')
