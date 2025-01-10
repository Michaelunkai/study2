# Specific VS Code path
$vsCodePath = "C:\backup\windowsapps\installed\Microsoft VS Code"

# Verify VS Code exists in the specified location
if (-not (Test-Path "$vsCodePath\code.exe")) {
    Write-Error "VS Code not found at $vsCodePath\code.exe. Please verify the path."
    exit 1
}

# Get the current user's PATH
$currentUserPath = [Environment]::GetEnvironmentVariable("Path", "User")

# Check if VS Code path is already in PATH
if ($currentUserPath -notlike "*$vsCodePath*") {
    # Add VS Code to PATH
    $newPath = $currentUserPath + ";$vsCodePath"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    
    # Update current session's PATH
    $env:Path = [Environment]::GetEnvironmentVariable("Path", "User") + ";" + [Environment]::GetEnvironmentVariable("Path", "Machine")
    
    Write-Host "VS Code successfully added to PATH"
} else {
    Write-Host "VS Code is already in PATH"
}

# Verify installation
try {
    $codeVersion = & "$vsCodePath\code.exe" --version
    Write-Host "VS Code version: $codeVersion"
    Write-Host "VS Code is now accessible from PowerShell!"
} catch {
    Write-Host "Please restart your PowerShell session for changes to take effect"
}
