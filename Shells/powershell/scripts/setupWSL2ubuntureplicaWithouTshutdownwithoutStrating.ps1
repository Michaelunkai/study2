# Set variables
$sourceDistro = "ubuntu"
$newDistro = "ubuntu2"
$destPath = "C:\wsl2\ubuntu2"
$tempExportPath = "$env:TEMP\ubuntu_temp.tar"

# Prepare destination directory
if (Test-Path $destPath) {
    Remove-Item -Path $destPath -Recurse -Force
}
New-Item -ItemType Directory -Path $destPath | Out-Null

# Remove existing distribution if it exists
if (wsl -l | Select-String -Pattern $newDistro) {
    wsl --unregister $newDistro
}

# Export using wsl.exe directly without shutting down the source distro
$exportProcess = Start-Process -FilePath "wsl.exe" -ArgumentList "--export $sourceDistro `"$tempExportPath`"" -PassThru -NoNewWindow
Wait-Process -InputObject $exportProcess

# Import and setup
if (Test-Path $tempExportPath) {
    wsl --import $newDistro $destPath $tempExportPath
    Remove-Item $tempExportPath

    # User setup with root username and password 123456
    wsl -d $newDistro -u root bash -c @"
useradd -m root
echo 'root:123456' | chpasswd
usermod -aG sudo root
echo 'root ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
"@

    # Set default user for the new distribution to root
    $registryPath = "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Lxss"
    $guid = (Get-ChildItem $registryPath | Where-Object { $_.GetValue("DistributionName") -eq $newDistro }).PSChildName
    if ($guid) {
        Set-ItemProperty -Path "$registryPath\$guid" -Name "DefaultUid" -Value 0
    }

    Write-Host "Import and setup of '$newDistro' completed successfully."
}

# The script finishes without starting WSL2.

