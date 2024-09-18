# Script to install PSWindowsUpdate module and perform Windows updates

# Install PSWindowsUpdate module with required parameters
Install-Module -Name PSWindowsUpdate -Force -AllowClobber -Scope CurrentUser

# Perform Windows updates
Get-WindowsUpdate -Install -AcceptAll -Verbose
