; AutoHotkey Script to Toggle Between Virtual Desktops using Shift + S

; Set the default desktop index
global currentDesktop := 1

; Shift + S to toggle between desktops
+S::
    if (currentDesktop = 1) {
        Send, ^#{Right} ; Switch to Desktop 2
        currentDesktop := 2
    } else {
        Send, ^#{Left} ; Switch to Desktop 1
        currentDesktop := 1
    }
return
