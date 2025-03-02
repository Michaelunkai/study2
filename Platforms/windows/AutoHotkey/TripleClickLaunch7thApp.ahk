; Triple-click detection for left mouse button with action for the 7th pinned app

~LButton::
    ; Check if this click is within 400 ms of the previous one.
    if (A_PriorHotkey = "~LButton" && A_TimeSincePriorHotkey < 400)
        clickCount++
    else
        clickCount := 1

    if (clickCount = 3)
    {
        clickCount := 0
        ; Launch the 7th pinned taskbar app using the Windows shortcut (Win+7)
        Send, #7
        ; Allow some time for the app to launch
        Sleep, 500
        ; Maximize the active window (adjust delay if necessary)
        WinMaximize, A
    }
return
