#SingleInstance Force

; Copy with Left Mouse Button + Right Mouse Button
~LButton & RButton::
{
    ClipSaved := ClipboardAll  ; Save the current clipboard
    Clipboard := ""            ; Clear the clipboard to detect changes
    Send, ^c                   ; Simulate CTRL+C for copying
    ClipWait, 1                ; Wait for the clipboard to update
    If (Clipboard != "")       ; Check if clipboard has content
    {
        ToolTip, Copied!       ; Show confirmation tooltip
        Sleep, 500
        ToolTip                ; Hide tooltip
    }
    Else
    {
        ToolTip, Copy Failed!  ; If no content was copied
        Sleep, 500
        ToolTip
    }
    Clipboard := ClipSaved     ; Restore original clipboard content
    Return
}

; Paste with Left Mouse Button + Middle Mouse Button
~LButton & MButton::
{
    If (Clipboard != "")       ; Ensure clipboard is not empty
    {
        Send, ^v               ; Simulate CTRL+V for pasting
        ToolTip, Pasted!       ; Show confirmation tooltip
        Sleep, 500
        ToolTip                ; Hide tooltip
    }
    Else
    {
        ToolTip, Nothing to Paste!  ; If clipboard is empty
        Sleep, 500
        ToolTip
    }
    Return
}
