# Ensure that you run this script as an administrator.

# Function to take ownership of a registry key
function Take-RegistryOwnership {
    param (
        [string]$RegistryPath
    )
    Write-Host "Taking ownership of $RegistryPath"
    Invoke-Expression "Set-ACL -Path '$RegistryPath' -AclObject (Get-Acl '$RegistryPath')"
}

# Disable Windows Defender Real-Time Protection
Set-MpPreference -DisableRealtimeMonitoring $true

# Disable Windows Defender Antivirus and Take Ownership
Write-Host "Disabling Windows Defender Antivirus..."
Take-RegistryOwnership -RegistryPath "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender"
New-Item -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender" -Force
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender" -Name "DisableAntiSpyware" -Value 1 -Force
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender" -Name "DisableAntiVirus" -Value 1 -Force

# Stop Windows Defender Antivirus Service (may require reboot)
Write-Host "Stopping and disabling Windows Defender Antivirus Service..."
sc.exe stop WinDefend
sc.exe config WinDefend start= disabled

# Disable Tamper Protection (requires manual action as it cannot be disabled programmatically)
Write-Host "Ensure Tamper Protection is disabled manually in Windows Security settings."

# Disable Windows Firewall for all profiles
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False

# Stop and Disable Windows Defender Firewall Service
Write-Host "Stopping and disabling Windows Defender Firewall Service..."
sc.exe stop mpssvc
sc.exe config mpssvc start= disabled

# Disable Security Center Notifications
Write-Host "Disabling Security Center notifications..."
Take-RegistryOwnership -RegistryPath "HKLM:\SOFTWARE\Microsoft\Security Center"
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Security Center" -Name "FirewallDisableNotify" -Value 1 -Force
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Security Center" -Name "DisableAntiVirusDisableNotify" -Value 1 -Force
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Security Center" -Name "DisableAntiSpywareDisableNotify" -Value 1 -Force

# Disable Windows Defender Scheduled Tasks
Write-Host "Disabling Windows Defender scheduled tasks..."
Get-ScheduledTask | Where-Object {$_.TaskName -like "*Windows Defender*"} | ForEach-Object {Disable-ScheduledTask -TaskName $_.TaskName -TaskPath $_.TaskPath}

# Confirm the status of Firewall and Defender
echo "Windows Firewall and Defender, including all components, should now be disabled."
Get-NetFirewallProfile
Get-MpPreference

