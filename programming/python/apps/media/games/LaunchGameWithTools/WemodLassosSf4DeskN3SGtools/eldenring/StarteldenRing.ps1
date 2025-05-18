# elden.ps1

# Ensure helper functions are defined or sourced if needed
function close {
    # Example close function body
    Write-Host "Running close..." -ForegroundColor Yellow
    # Add your close logic here
}

function superf4 {
    # Example superf4 function body
    Write-Host "Running SuperF4..." -ForegroundColor Yellow
    # Add your SuperF4 logic here
}

function desk {
    # Example desk function body
    Write-Host "Switching desktops..." -ForegroundColor Yellow
    # Add your AHK desktop switch logic here
}

# Run the full sequence
close
superf4
desk

# Run suspend/resume script
& "F:\study\shells\powershell\scripts\susEldenRing.ps1"

# Wait before launching
Start-Sleep -Seconds 10

# Launch Elden Ring + WeMod EXE
Start-Process "C:\Users\micha\Desktop\runERandWemod.exe"

# Small delay to ensure the window is ready
Start-Sleep -Seconds 2

# Simulate pressing "1" key
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.SendKeys]::SendWait("1")

