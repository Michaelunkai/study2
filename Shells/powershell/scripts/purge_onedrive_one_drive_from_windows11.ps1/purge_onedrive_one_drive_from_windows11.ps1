# Run as Administrator with highest privileges
Set-ExecutionPolicy Bypass -Scope Process -Force

# Kill ALL related processes brutally
taskkill /F /IM "OneDrive.exe" 2>$null
taskkill /F /IM "FileCoAuth.exe" 2>$null
taskkill /F /IM "Setup.exe" 2>$null

# Protected paths
$exclusions = @(
    "C:\study",
    "C:\backup"
)

# Take ownership of EVERYTHING in C: (except excluded folders)
Write-Host "Taking ownership of files..." -ForegroundColor Red
$takeownCommand = @"
cmd /c for /f "tokens=*" %a in ('dir /b /s /a "C:\*onedrive*"') do (
    if not "%a" == "" (
        echo Processing: %a
        takeown /f "%a" /a /r /d y
        icacls "%a" /grant administrators:F /t
        icacls "%a" /grant system:F /t
    )
)
"@
Invoke-Expression -Command $takeownCommand

# Force delete function using multiple methods
function Destroy-Path {
    param([string]$path)
    if ($exclusions | Where-Object { $path -like "$_*" }) {
        return
    }
    
    try {
        # Method 1: Direct force delete
        Remove-Item -Path $path -Force -Recurse -ErrorAction SilentlyContinue
        
        # Method 2: CMD del
        cmd /c "del /f /s /q `"$path`"" 2>$null
        
        # Method 3: CMD rd for folders
        cmd /c "rd /s /q `"$path`"" 2>$null
        
        # Method 4: Use handle.exe if available
        if (Test-Path "handle.exe") {
            handle.exe -accepteula -closeall "$path" 2>$null
            Remove-Item -Path $path -Force -Recurse -ErrorAction SilentlyContinue
        }
    } catch { }
}

Write-Host "Starting aggressive removal..." -ForegroundColor Red

# Get ALL paths containing 'onedrive' using cmd (more thorough than PowerShell)
$findCommand = @"
cmd /c dir /b /s /a "C:\*onedrive*" 2>nul
cmd /c dir /b /s /a "C:\*ONEDRIVE*" 2>nul
"@

# Execute find and destroy
$paths = Invoke-Expression -Command $findCommand
$paths | ForEach-Object {
    $path = $_
    if (-not [string]::IsNullOrWhiteSpace($path)) {
        Write-Host "Destroying: $path" -ForegroundColor Yellow
        Destroy-Path $path
    }
}

# Direct attack on known locations
$knownPaths = @(
    "C:\Windows\System32\OneDriveSetup.exe",
    "C:\Windows\SysWOW64\OneDriveSetup.exe",
    "C:\Windows\System32\OneDrive.ico",
    "C:\Program Files*\Microsoft OneDrive",
    "C:\Program Files*\WindowsApps\*onedrive*",
    "C:\Windows\ServiceProfiles\LocalService\AppData\Local\Microsoft\OneDrive",
    "C:\Windows\ServiceProfiles\NetworkService\AppData\Local\Microsoft\OneDrive",
    "$env:LOCALAPPDATA\Microsoft\OneDrive",
    "$env:LOCALAPPDATA\OneDrive",
    "$env:SYSTEMROOT\System32\OneDriveSetup.exe",
    "$env:SYSTEMROOT\SysWOW64\OneDriveSetup.exe"
)

$knownPaths | ForEach-Object {
    Get-Item -Path $_ -ErrorAction SilentlyContinue | ForEach-Object {
        Write-Host "Destroying known location: $_" -ForegroundColor Red
        Destroy-Path $_
    }
}

# Attack Windows Apps specifically
$windowsAppsPath = "C:\Program Files\WindowsApps"
if (Test-Path $windowsAppsPath) {
    Get-ChildItem -Path $windowsAppsPath -Recurse -Force -ErrorAction SilentlyContinue | 
        Where-Object { $_.Name -like "*onedrive*" } | 
        ForEach-Object {
            Write-Host "Destroying WindowsApps item: $_" -ForegroundColor Red
            Destroy-Path $_.FullName
        }
}

# Final sweep using direct system commands
Write-Host "Performing final sweep..." -ForegroundColor Red
cmd /c "del /f /s /q C:\*onedrive* 2>nul"
cmd /c "rd /s /q C:\*onedrive* 2>nul"

Write-Host "`nOperation completed. Some files might require manual removal in Safe Mode." -ForegroundColor Green
Write-Host "Protected folders preserved: $($exclusions -join ', ')" -ForegroundColor Cyan
