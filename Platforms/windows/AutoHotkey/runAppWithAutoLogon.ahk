Run, "full apth to .exe"
Sleep, 5000  ; Wait 5 seconds for Parsec to open

; Send email
Send, yourmail@gmail.com
Sleep, 500
Send, {Tab}  ; Move to password field
Sleep, 500
SendRaw, yourpassword
Sleep, 500
Send, {Enter}  ; Submit login
