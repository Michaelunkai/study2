# Get the Firefox process
$firefoxProcess = Get-Process -Name firefox

# Display the current priority
Write-Host "Firefox Process Priority: $($firefoxProcess.PriorityClass)"
