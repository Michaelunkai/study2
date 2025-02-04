# Required for cursor manipulation
Add-Type -AssemblyName System.Windows.Forms

# Function to get the secondary screen
function Get-SecondaryScreen {
    $screens = [System.Windows.Forms.Screen]::AllScreens
    return $screens | Where-Object { -not $_.Primary }
}

# Function to move the cursor to the center of the secondary screen
function Move-CursorToSecondaryScreen {
    $secondaryScreen = Get-SecondaryScreen
    if ($secondaryScreen) {
        $centerX = $secondaryScreen.Bounds.Left + ($secondaryScreen.Bounds.Width / 2)
        $centerY = $secondaryScreen.Bounds.Top + ($secondaryScreen.Bounds.Height / 2)
        [System.Windows.Forms.Cursor]::Position = New-Object System.Drawing.Point($centerX, $centerY)
    }
}

# Main loop
try {
    while ($true) {
        $currentPosition = [System.Windows.Forms.Cursor]::Position
        $secondaryScreen = Get-SecondaryScreen

        if ($secondaryScreen) {
            # Check if the cursor is outside the secondary screen
            if (
                $currentPosition.X -lt $secondaryScreen.Bounds.Left -or
                $currentPosition.X -ge $secondaryScreen.Bounds.Right -or
                $currentPosition.Y -lt $secondaryScreen.Bounds.Top -or
                $currentPosition.Y -ge $secondaryScreen.Bounds.Bottom
            ) {
                Move-CursorToSecondaryScreen
            }
        } else {
            Write-Host "No secondary screen detected. Please connect a second screen and restart the script."
            break
        }

        # Wait for a short time before checking again
        Start-Sleep -Milliseconds 100
    }
}
finally {
    Write-Host "Script stopped."
}
