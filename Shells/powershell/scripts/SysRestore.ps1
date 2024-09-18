# Script Name: SysRestore.ps1

# Path for temporary system restore point
$tempPath = "D:\Win11Restore"

# Path for final system restore point
$finalPath = "D:\new\Win11Restore"

# Timestamp
$time = Get-Date -Format "yyyyMMddHHmmss"

# Start process to create system restore point in the background
Start-Process powershell -ArgumentList "-Command Checkpoint-Computer -Description 'Win11 Restore - $time' -RestorePointType 'MODIFY_SETTINGS'" -WindowStyle Hidden

# Wait for a moment to ensure the restore point is created
Start-Sleep -Seconds 10

# Move the created restore point to the final directory
Move-Item -Path "$tempPath\RestorePoint-$time" -Destination $finalPath -Force

Write-Host "SysRestore created successfully at: $finalPath\Rest_$time"

# Modify registry to allow more frequent restore points (for testing purposes)
$regPath = "HKLM:\Software\Microsoft\Windows NT\CurrentVersion\SystemRestore"
$regName = "SystemRestorePointCreationFrequency"
$regValue = 1  # Set the desired frequency in minutes (1 minute in this example)

# Create or update the registry value
New-ItemProperty -Path $regPath -Name $regName -Value $regValue -PropertyType DWORD -Force
