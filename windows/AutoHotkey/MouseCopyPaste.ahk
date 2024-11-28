;
; AutoHotkey Script for Mouse Actions
;
; Double Right-Click: Copy
; Triple Left-Click: Paste
;

; Detecting double-click with the right mouse button for Copy
~RButton::
    ClickCount++
    if (ClickCount = 2) {
        ClickCount := 0 ; Reset counter
        Send, ^c ; Copy
    }
    SetTimer, ResetClickCount, -400 ; Timer to reset click count after 400 ms
return

; Detecting triple-click with the left mouse button for Paste
~LButton::
    ClickCountLeft++
    if (ClickCountLeft = 3) {
        ClickCountLeft := 0 ; Reset counter
        Send, ^v ; Paste
    }
    SetTimer, ResetClickCountLeft, -400 ; Timer to reset click count after 400 ms
return

; Timers to reset click counters
ResetClickCount:
    ClickCount := 0
return

ResetClickCountLeft:
    ClickCountLeft := 0
return
