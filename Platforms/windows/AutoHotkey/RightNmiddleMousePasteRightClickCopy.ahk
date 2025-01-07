#SingleInstance Force

; Initialize variables
LButtonPressed := false
ClipSaved := ""

; Track left button press
~LButton::
{
    LButtonPressed := true
    return
}

; Track left button release
~LButton Up::
{
    LButtonPressed := false
    return
}

; Copy when left + right mouse buttons are pressed
~RButton::
{
    if (LButtonPressed) {
        ; Save current clipboard
        ClipSaved := ClipboardAll
        
        ; Clear clipboard and attempt to copy
        Clipboard := ""
        Send ^c
        
        ; Wait for clipboard to contain data
        ClipWait, 1
        if (Clipboard != "") {
            ToolTip, Copied!
            Sleep, 500
            ToolTip
        } else {
            ToolTip, Copy Failed!
            Sleep, 500
            ToolTip
        }
    }
    return
}

; Paste when left + middle mouse buttons are pressed
~MButton::
{
    if (LButtonPressed && Clipboard != "") {
        ; Delete any selected text first
        Send {Delete}
        
        ; Then paste the clipboard content
        Send ^v
        
        ToolTip, Pasted!
        Sleep, 500
        ToolTip
    } else if (LButtonPressed) {
        ToolTip, Nothing to Paste!
        Sleep, 500
        ToolTip
    }
    return
}
