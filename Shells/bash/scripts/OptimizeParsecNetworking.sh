# Requires admin privileges
#Requires -RunAsAdministrator

# Function to test if admin
function Test-Administrator {
    $user = [Security.Principal.WindowsIdentity]::GetCurrent();
    (New-Object Security.Principal.WindowsPrincipal $user).IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
}

# Check for admin rights
if (-not (Test-Administrator)) {
    Write-Host "Please run this script as Administrator" -ForegroundColor Red
    exit
}

# Function to test network connectivity
function Test-NetworkConnectivity {
    $testResults = @()
    $testResults += Test-NetConnection -ComputerName "game.parsecgaming.com" -Port 443
    $testResults += Test-NetConnection -ComputerName "game.parsecgaming.com" -Port 22222
    $testResults += Test-NetConnection -ComputerName "game.parsecgaming.com" -Port 22223
    return $testResults
}

# Function to optimize network settings
function Set-NetworkOptimization {
    # Enable TCP Fast Open
    Set-NetTCPSetting -SettingName InternetCustom -AutoTuningLevelLocal Normal
    
    # Disable auto-tuning (can sometimes interfere with streaming)
    netsh int tcp set global autotuninglevel=disabled
    
    # Optimize QoS settings
    netsh int tcp set global congestionprovider=ctcp
    
    # Reset Winsock catalog
    netsh winsock reset
    
    # Reset TCP/IP stack
    netsh int ip reset
    
    # Clear DNS cache
    ipconfig /flushdns
}

# Function to configure Windows Firewall
function Set-ParsecFirewall {
    # Remove existing Parsec rules
    Get-NetFirewallRule | Where-Object {$_.DisplayName -like "*Parsec*"} | Remove-NetFirewallRule
    
    # Add new Parsec rules
    New-NetFirewallRule -DisplayName "Parsec UDP" -Direction Inbound -Action Allow -Protocol UDP -LocalPort 22222-22223
    New-NetFirewallRule -DisplayName "Parsec TCP" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 22222-22223
}

# Function to optimize Windows settings
function Set-WindowsOptimization {
    # Disable Network Power Management
    Get-NetAdapter | ForEach-Object {
        $adapter = $_
        Disable-NetAdapterPowerManagement -Name $adapter.Name
    }
    
    # Set power plan to high performance
    powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
    
    # Disable WiFi Sense
    Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\WcmSvc\wifinetworkmanager\config" -Name "AutoConnectAllowedOEM" -Value 0
}

# Function to verify Parsec installation
function Test-ParsecInstallation {
    $parsecPath = "${env:APPDATA}\Parsec"
    if (-not (Test-Path $parsecPath)) {
        Write-Host "Parsec installation not found. Please reinstall Parsec." -ForegroundColor Red
        return $false
    }
    return $true
}

# Main execution
Write-Host "Starting Parsec connection optimization..." -ForegroundColor Cyan

# Check Parsec installation
if (-not (Test-ParsecInstallation)) {
    exit
}

# Run all optimizations
Write-Host "Testing network connectivity..."
$networkTests = Test-NetworkConnectivity

Write-Host "Configuring network optimizations..."
Set-NetworkOptimization

Write-Host "Configuring firewall rules..."
Set-ParsecFirewall

Write-Host "Optimizing Windows settings..."
Set-WindowsOptimization

# Final cleanup and restart recommendation
Write-Host "`nOptimization complete. Please:" -ForegroundColor Green
Write-Host "1. Restart your computer"
Write-Host "2. Ensure both devices are on the same network or have direct internet access"
Write-Host "3. Check if your antivirus is not blocking Parsec"
Write-Host "4. Verify that UDP ports 22222-22223 are open on both devices"

# Create verification report
$report = @{
    "Timestamp" = Get-Date
    "NetworkTests" = $networkTests
    "ParsecInstalled" = Test-ParsecInstallation
    "FirewallRules" = Get-NetFirewallRule | Where-Object {$_.DisplayName -like "*Parsec*"}
}

$report | Export-Clixml "$env:USERPROFILE\Desktop\ParsecOptimizationReport.xml"
