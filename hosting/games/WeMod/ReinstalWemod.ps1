# Stop all WeMod processes
Get-Process -Name "*WeMod*","*wemod*" -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 3
taskkill /F /IM "WeMod.exe" /T 2>$null
taskkill /F /IM "WeMod*.exe" /T 2>$null

# Stop any WeMod-related services
Get-Service | Where-Object {$_.Name -like "*WeMod*" -or $_.DisplayName -like "*WeMod*"} | Stop-Service -Force -ErrorAction SilentlyContinue
Get-Service | Where-Object {$_.Name -like "*wemod*" -or $_.DisplayName -like "*wemod*"} | Stop-Service -Force -ErrorAction SilentlyContinue

# Set error action preference
$ErrorActionPreference = "SilentlyContinue"

# Remove hidden attributes from directories
if (Test-Path "C:\Users\$env:USERNAME\AppData\Roaming\WeMod\games\logs") { 
    attrib -R -S -H "C:\Users\$env:USERNAME\AppData\Roaming\WeMod\games\logs\*.*" /S /D 
}

if (Test-Path "C:\Users\$env:USERNAME\AppData\Local\WeMod\app-*\resources\app.asar.unpacked\static\unpacked\overlay") { 
    attrib -R -S -H "C:\Users\$env:USERNAME\AppData\Local\WeMod\app-*\resources\app.asar.unpacked\static\unpacked\overlay\*.*" /S /D 
}

if (Test-Path "C:\Users\$env:USERNAME\AppData\Local\WeMod\app-*\resources\app.asar.unpacked\static\unpacked\trainerlib") { 
    attrib -R -S -H "C:\Users\$env:USERNAME\AppData\Local\WeMod\app-*\resources\app.asar.unpacked\static\unpacked\trainerlib\*.*" /S /D 
}

# Grant full permissions to ensure removal is possible
Start-Sleep -Seconds 1
icacls "C:\Users\$env:USERNAME\AppData\Local\WeMod" /grant Everyone:F /T /C /Q
icacls "C:\Users\$env:USERNAME\AppData\Roaming\WeMod" /grant Everyone:F /T /C /Q
Start-Sleep -Seconds 1

# Force purge specific paths
$pathsToDelete = @(
    "C:\Users\$env:USERNAME\AppData\Local\Temp\WinGet\WeMod.WeMod.10.8.1",
    "C:\Users\$env:USERNAME\AppData\Local\Temp\WinGet\cache\V2_PVD\Microsoft.Winget.Source_8wekyb3d8bbwe\packages\WeMod.WeMod",
    "C:\Users\$env:USERNAME\AppData\Roaming\WeMod",
    "C:\Users\$env:USERNAME\AppData\Local\Temp\WinGet\cache\V2_M\Microsoft.Winget.Source_8wekyb3d8bbwe\manifests\w\WeMod\WeMod",
    "C:\Users\$env:USERNAME\AppData\Local\Temp\WinGet\cache\V2_M\Microsoft.Winget.Source_8wekyb3d8bbwe\manifests\w\WeMod",
    "C:\Users\$env:USERNAME\AppData\Local\WeMod"
)

foreach ($path in $pathsToDelete) {
    if (Test-Path $path) {
        # Take ownership and grant full permissions
        takeown /F $path /R /D Y
        icacls $path /grant Everyone:F /T /C /Q
        
        # Forcefully remove the directory
        Remove-Item $path -Recurse -Force -ErrorAction SilentlyContinue
        
        # Double-check if directory still exists and try alternative removal method
        if (Test-Path $path) {
            cmd /c "rd /s /q `"$path`""
        }
    }
}

# Remove standard WeMod directories
Remove-Item "C:\Users\$env:USERNAME\AppData\Local\WeMod" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "C:\Users\$env:USERNAME\AppData\Roaming\WeMod" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "C:\Users\$env:USERNAME\AppData\LocalLow\WeMod" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "C:\Program Files (x86)\WeMod" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "C:\Program Files\WeMod" -Recurse -Force -ErrorAction SilentlyContinue

# Remove registry entries
Remove-Item "HKCU:\Software\WeMod" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "HKLM:\Software\WeMod" -Recurse -Force -ErrorAction SilentlyContinue

# Remove uninstall registry entries
Get-Item "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*" -ErrorAction SilentlyContinue | 
    Where-Object { $_.GetValue("DisplayName") -like "*WeMod*" } | 
    Remove-Item -Recurse -Force

# Clean temp directories
$tempPath = [System.IO.Path]::GetTempPath()
Get-ChildItem -Path $tempPath -Filter "*WeMod*" -Recurse -ErrorAction SilentlyContinue | 
    Remove-Item -Recurse -Force

# Final sweep of all WeMod-related files in AppData
Get-ChildItem -Path "C:\Users\$env:USERNAME\AppData" -Filter "*WeMod*" -Recurse -ErrorAction SilentlyContinue | 
    Remove-Item -Recurse -Force

# Install WeMod
winget install WeMod.WeMod
