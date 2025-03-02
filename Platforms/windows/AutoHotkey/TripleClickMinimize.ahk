~LButton::
    ; Check if this click is within 400ms of the previous one
    if (A_PriorHotkey <> "~LButton" or A_TimeSincePriorHotkey > 400)
        ClickCount := 1
    else
        ClickCount++
    
    if (ClickCount = 3) {
        Send, #{d}   ; #{d} sends Windows + D
        ClickCount := 0  ; reset the counter after triggering the action
    }
return
