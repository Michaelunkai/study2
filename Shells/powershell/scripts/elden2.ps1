# elden2.ps1

# Run the 'close' function or command
close

# Run the 'superf4' function or command
superf4

# Run the 'desk' function or command
desk

# Run the suspend Elden Ring script
& "F:\study\shells\powershell\scripts\susEldenRing.ps1"

# Wait 10 seconds for the above script to execute
Start-Sleep -Seconds 10

# Launch the EXE that runs Elden Ring and WeMod
Start-Process "C:\Users\micha\Desktop\runERandWemod.exe"

# Wait briefly before sending the key
Start-Sleep -Seconds 2

# Load Windows Forms to allow sending keystrokes
Add-Type -AssemblyName System.Windows.Forms

# Send the key "1" as if it was pressed
[System.Windows.Forms.SendKeys]::SendWait("1")
