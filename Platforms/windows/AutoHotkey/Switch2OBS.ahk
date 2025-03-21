; Store the last active window
global lastWindow := ""

+F::  ; Shift + F to switch to OBS
    lastWindow := WinExist("A") ; Save the current active window
    IfWinExist, ahk_exe obs64.exe
    {
        WinActivate ; Switch to OBS
    }
    else
    {
        Run, "C:\Program Files\obs-studio\bin\64bit\obs64.exe" ; Launch OBS if it's not running
    }
return

+G::  ; Shift + G to switch back to the previous window
    if (lastWindow)
    {
        WinActivate, ahk_id %lastWindow% ; Switch back to the last active window
    }
return
