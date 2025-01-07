; Define screen dimensions
SysGet, ScreenWidth, 78
SysGet, ScreenHeight, 79
ThirdWidth := ScreenWidth / 3

; Snap window to the left third
^!1::
    WinGet, currentWindow, ID, A
    WinMove, ahk_id %currentWindow%, , 0, 0, ThirdWidth, ScreenHeight
return

; Snap window to the middle third
^!2::
    WinGet, currentWindow, ID, A
    WinMove, ahk_id %currentWindow%, , ThirdWidth, 0, ThirdWidth, ScreenHeight
return

; Snap window to the right third
^!3::
    WinGet, currentWindow, ID, A
    WinMove, ahk_id %currentWindow%, , 2*ThirdWidth, 0, ThirdWidth, ScreenHeight
return

