# Ensure that you run this script as an administrator.

# Re-enable Windows Defender Real-Time Protection
Set-MpPreference -DisableRealtimeMonitoring $false

# Re-enable Windows Defender Antivirus
Write-Host "Re-enabling Windows Defender Antivirus..."
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender" -Name "DisableAntiSpyware" -Value 0 -Force
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender" -Name "DisableAntiVirus" -Value 0 -Force

# Start and Enable Windows Defender Antivirus Service
sc.exe config WinDefend start= auto
sc.exe start WinDefend

# Re-enable Windows Firewall for all profiles
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True

# Start and Enable Windows Defender Firewall Service
Write-Host "Starting and enabling Windows Defender Firewall Service..."
sc.exe config mpssvc start= auto
sc.exe start mpssvc

# Enable Security Center Notifications
Write-Host "Re-enabling Security Center notifications..."
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Security Center" -Name "FirewallDisableNotify" -Value 0 -Force
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Security Center" -Name "DisableAntiVirusDisableNotify" -Value 0 -Force
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Security Center" -Name "DisableAntiSpywareDisableNotify" -Value 0 -Force

# Re-enable Windows Defender Scheduled Tasks
Write-Host "Re-enabling Windows Defender scheduled tasks..."
Get-ScheduledTask | Where-Object {$_.TaskName -like "*Windows Defender*"} | ForEach-Object {Enable-ScheduledTask -TaskName $_.TaskName -TaskPath $_.TaskPath}

# Confirm the status of Firewall and Defender
echo "Windows Firewall and Defender, including all components, should now be re-enabled."
Get-NetFirewallProfile
Get-MpPreference
