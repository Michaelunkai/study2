# Set variables
$sourceDistro = "ubuntu"
$newDistro = "ubuntu2"
$sourcePath = "C:\wsl2\ubuntu\ext4.vhdx"
$destPath = "C:\wsl2\ubuntu2"

# Function to safely remove a directory and its contents
function Remove-DirectorySafely {
    param([string]$path)
    if (Test-Path $path) {
        Write-Host "Removing existing directory: $path"
        Remove-Item -Path $path -Recurse -Force
    }
}

# Create or clean destination directory
Remove-DirectorySafely $destPath
New-Item -ItemType Directory -Path $destPath | Out-Null

# Check if the new distribution already exists
if (wsl -l | Select-String -Pattern $newDistro) {
    Write-Host "Removing existing distribution: $newDistro"
    wsl --unregister $newDistro
}

# Export the source distribution
$tempExportPath = "$env:TEMP\ubuntu_temp.tar"
Write-Host "Exporting $sourceDistro to $tempExportPath..."
wsl --export $sourceDistro $tempExportPath
if (-not $?) {
    Write-Host "Failed to export $sourceDistro. Exiting." -ForegroundColor Red
    exit
}

# Import the new distribution
Write-Host "Importing $newDistro from $tempExportPath..."
wsl --import $newDistro $destPath $tempExportPath
if (-not $?) {
    Write-Host "Failed to import $newDistro. Exiting." -ForegroundColor Red
    Remove-Item $tempExportPath -ErrorAction SilentlyContinue
    exit
}

# Clean up the temporary export file
Remove-Item $tempExportPath -ErrorAction SilentlyContinue

# Verify the new distribution was created
if (-not (wsl -l | Select-String -Pattern $newDistro)) {
    Write-Host "Failed to create $newDistro. Exiting." -ForegroundColor Red
    exit
}

# Set the default user for the new distribution (assumes the default user in the source distro is "root")
Write-Host "Setting up default user..."
wsl -d $newDistro -u root useradd -m user
wsl -d $newDistro -u root passwd user
wsl -d $newDistro -u root usermod -aG sudo user
wsl -d $newDistro -u root bash -c "echo 'user ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers"

# Set the default user for the new distribution
$registryPath = "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Lxss"
$guid = (Get-ChildItem $registryPath | Where-Object { $_.GetValue("DistributionName") -eq $newDistro }).PSChildName
if ($guid) {
    Set-ItemProperty -Path "$registryPath\$guid" -Name "DefaultUid" -Value 1000
} else {
    Write-Host "Failed to set default user in registry. You may need to set it manually." -ForegroundColor Yellow
}

# Launch the new distribution
Write-Host "Launching $newDistro..."
wsl -d $newDistro

Write-Host "$newDistro WSL distribution has been created and launched." -ForegroundColor Green