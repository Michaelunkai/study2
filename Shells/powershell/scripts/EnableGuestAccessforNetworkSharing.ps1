# Define the registry path and key
$RegistryPath = "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanWorkstation\Parameters"
$RegistryKey = "AllowInsecureGuestAuth"

# Check if the key exists
if (-not (Test-Path -Path "$RegistryPath\$RegistryKey")) {
    # Create the registry key if it doesn't exist
    New-ItemProperty -Path $RegistryPath -Name $RegistryKey -PropertyType DWORD -Value 1
    Write-Host "Registry key created and set to enable guest access."
} else {
    # Update the value if the key already exists
    Set-ItemProperty -Path $RegistryPath -Name $RegistryKey -Value 1
    Write-Host "Registry key updated to enable guest access."
}

# Restart the Workstation service to apply changes
Restart-Service -Name LanmanWorkstation -Force
Write-Host "Workstation service restarted. Guest access is now enabled."
