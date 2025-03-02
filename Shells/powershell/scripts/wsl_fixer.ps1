# Ensure the script is run with administrative privileges
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "Please run this script as an Administrator."
    exit
}

# Update WSL
Write-Host "Updating WSL..."
wsl --update

# Ensure WSL 2 is installed and set as the default version
Write-Host "Ensuring WSL 2 is installed and set as the default version..."
wsl --set-default-version 2

# Check for and install any missing WSL components
Write-Host "Checking for and installing missing WSL components..."
$wslComponents = "Microsoft-Windows-Subsystem-Linux", "VirtualMachinePlatform"
foreach ($component in $wslComponents) {
    if (-not (Get-WindowsOptionalFeature -FeatureName $component -Online | Where-Object { $_.State -eq 'Enabled' })) {
        Enable-WindowsOptionalFeature -Online -FeatureName $component -NoRestart
    }
}

# Restart the WSL service
Write-Host "Restarting the WSL service..."
Restart-Service LxssManager

# Check for and install the latest Windows updates
Write-Host "Checking for and installing the latest Windows updates..."
Install-Module -Name PSWindowsUpdate -Force -SkipPublisherCheck
Import-Module PSWindowsUpdate
Install-WindowsUpdate -AcceptAll -AutoReboot

Write-Host "Script completed. Please restart your computer if prompted."

