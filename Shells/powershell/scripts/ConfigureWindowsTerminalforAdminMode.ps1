# Navigate to Windows Terminal settings location
$settingsPath = "$env:LOCALAPPDATA\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json"

# Create backup
Copy-Item $settingsPath "$settingsPath.backup"

# Get current settings
$settings = Get-Content $settingsPath | ConvertFrom-Json

# Add elevation to defaults
$settings.profiles.defaults | Add-Member -Type NoteProperty -Name "elevate" -Value $true -Force

# Save modified settings
$settings | ConvertTo-Json -Depth 32 | Set-Content $settingsPath
