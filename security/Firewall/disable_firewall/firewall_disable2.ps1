# Ensure that you run this script as an administrator.

# Function to take ownership of a registry key properly
function Take-RegistryOwnership {
    param(
        [string]$RegistryPath
    )
    Write-Host "Taking ownership of $RegistryPath"

    # Convert 'HKLM:\...' to standard registry path for .NET
    $regSubPath = $RegistryPath -replace "HKLM:\\", ""

    # Open the registry key with TakeOwnership rights
    $key = [Microsoft.Win32.Registry]::LocalMachine.OpenSubKey($regSubPath, [System.Security.AccessControl.RegistryRights]::TakeOwnership)
    $acl = $key.GetAccessControl()

    # Set the owner to Administrators
    $acl.SetOwner([System.Security.Principal.NTAccount]"Administrators")
    $key.SetAccessControl($acl)

    # Reload the ACL and grant Administrators full control
    $acl = $key.GetAccessControl()
    $rule = New-Object System.Security.AccessControl.RegistryAccessRule(
        "Administrators",
        "FullControl",
        "ObjectInherit,ContainerInherit",
        "None",
        "Allow"
    )
    $acl.AddAccessRule($rule)
    $key.SetAccessControl($acl)
    $key.Close()
}

# Disable Windows Defender Real-Time Protection
Set-MpPreference -DisableRealtimeMonitoring $true

# Disable Windows Defender Antivirus in Registry
Write-Host "Disabling Windows Defender Antivirus..."
Take-RegistryOwnership -RegistryPath "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender"
New-Item -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender" -Force | Out-Null
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender" -Name "DisableAntiSpyware" -Value 1 -Force
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender" -Name "DisableAntiVirus" -Value 1 -Force

# Stop and disable Windows Defender Antivirus service
Write-Host "Stopping and disabling Windows Defender Antivirus Service..."
sc.exe stop WinDefend
sc.exe config WinDefend start= disabled

# Note: Tamper Protection must be turned off manually in Windows Security (no direct script method).
Write-Host "Ensure Tamper Protection is disabled manually in Windows Security settings."

# Disable Windows Firewall for Domain, Public, and Private
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False

# Stop and disable Windows Defender Firewall Service
Write-Host "Stopping and disabling Windows Defender Firewall Service..."
sc.exe stop mpssvc
sc.exe config mpssvc start= disabled

# Disable Security Center notifications
Write-Host "Disabling Security Center notifications..."
Take-RegistryOwnership -RegistryPath "HKLM:\SOFTWARE\Microsoft\Security Center"
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Security Center" -Name "FirewallDisableNotify" -Value 1 -Force
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Security Center" -Name "DisableAntiVirusDisableNotify" -Value 1 -Force
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Security Center" -Name "DisableAntiSpywareDisableNotify" -Value 1 -Force

# Disable Windows Defender Scheduled Tasks
Write-Host "Disabling Windows Defender scheduled tasks..."
Get-ScheduledTask | Where-Object { $_.TaskName -like "*Windows Defender*" } | ForEach-Object {
    Disable-ScheduledTask -TaskName $_.TaskName -TaskPath $_.TaskPath
}

# Final confirmation
Write-Host "`nWindows Firewall and Windows Defender, including all components, should now be fully disabled."
Get-NetFirewallProfile
Get-MpPreference

