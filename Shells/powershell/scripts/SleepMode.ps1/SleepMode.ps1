# Enable Hibernate (if not already enabled)
powercfg /hibernate on

# Disable the requirement to enter a password after waking up
powercfg /SETACVALUEINDEX SCHEME_CURRENT SUB_NONE CONSOLELOCK 0
powercfg /SETDCVALUEINDEX SCHEME_CURRENT SUB_NONE CONSOLELOCK 0
powercfg /apply

# Set the system to hibernate immediately
Stop-Process -Name "OneDrive" -Force -ErrorAction SilentlyContinue
rundll32.exe powrprof.dll,SetSuspendState Hibernate

# Disable wake from all devices except the keyboard
$devices = Get-WmiObject -Query "SELECT * FROM Win32_PnPEntity WHERE Description LIKE '%Keyboard%'"

# Iterate through all devices to configure wake-up capabilities
foreach ($device in $devices) {
    $deviceID = $device.DeviceID -replace "\\", "\\\\" # Escape backslashes for PowerShell compatibility
    $powerManagement = Get-WmiObject -Query "SELECT * FROM Win32_DeviceSettings WHERE InstanceID='$deviceID'" `
        -ErrorAction SilentlyContinue
    if ($powerManagement -ne $null) {
        # Allow only the keyboard to wake the system
        powercfg -deviceenablewake $device.Name
    }
}

# Disable wake-up for all other devices
$allDevices = powercfg -devicequery wake_armed
foreach ($dev in $allDevices) {
    if ($dev -notlike "*Keyboard*") {
        powercfg -devicedisablewake $dev
    }
}

# Ensure system locks before hibernation is disabled
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v InactivityTimeoutSecs /t REG_DWORD /d 0 /f
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\System" /v AllowDomainPINLogon /t REG_DWORD /d 1 /f

# Ensure user session resumes directly after wake-up
rundll32.exe powrprof.dll,SetSuspendState Hibernate
