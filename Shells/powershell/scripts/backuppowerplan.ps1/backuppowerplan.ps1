# BackupPowerPlans.ps1

# Specify the output directory for the backup
$backupDirectory = "C:\backup\windowsapps\powerplans"

# Specify the Power Scheme GUIDs and their corresponding names
$powerPlans = @{
    "27fa6203-3987-4dcc-918d-748559d549ec" = "Performance"
    "381b4222-f694-41f0-9685-ff5bb260df2e" = "Balanced"
    "64a64f24-65b9-4b56-befd-5ec1eaced9b3" = "Silent"
}

# Create the backup directory if it doesn't exist
if (-not (Test-Path $backupDirectory)) {
    New-Item -ItemType Directory -Path $backupDirectory | Out-Null
}

# Loop through each Power Plan and create a bat file
foreach ($guid in $powerPlans.Keys) {
    $planName = $powerPlans[$guid]
    $batFilePath = Join-Path $backupDirectory "$planName.bat"

    # Create the bat file content
    $batContent = @"
powercfg /s $guid
"@

    # Write the content to the bat file
    $batContent | Out-File -FilePath $batFilePath -Force
}

Write-Host "Power plans backed up to $backupDirectory"
