^F3:: {
    try {
        ; Get the HWND of the active (foreground) window
        hwnd := WinGetID("A")
        if !hwnd {
            MsgBox "No active window found."
            return
        }

        ; Get the process ID (PID) of the window
        pid := WinGetPID(hwnd)
        if !pid {
            MsgBox "Failed to get process ID."
            return
        }

        ; Try to close nicely first (can skip if always force is preferred)
        ProcessClose(pid)

        ; Double-check if process is still alive
        Sleep 200
        if ProcessExist(pid) {
            ; If still running, forcefully kill via WMI (low-level)
            try {
                wmi := ComObject("winmgmts:\\.\root\cimv2")
                for proc in wmi.ExecQuery("Select * from Win32_Process Where ProcessId = " pid) {
                    proc.Terminate()  ; WMI-based kill is lower-level than ProcessClose
                }
            } catch {
                MsgBox "WMI force-kill failed."
            }
        }
    } catch {
        MsgBox "Unexpected error during process termination."
    }
}

