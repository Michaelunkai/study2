# Uninstall Hyper-V Role
Disable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V-All

# Remove Hyper-V virtual switches
Get-VMSwitch | Remove-VMSwitch

# Remove Virtual Switches that were created by Hyper-V
Get-NetAdapter | ?{$_.Name -like "vEthernet*"} | Remove-NetAdapter

# Remove Hyper-V Management Tools
Get-WindowsFeature -Name RSAT-Hyper-V-Tools | Uninstall-WindowsFeature

# Remove Hyper-V PowerShell Module
Uninstall-Module -Name Hyper-V -Force -AllVersions

# Reboot the system to finalize the removal
Restart-Computer -Force
