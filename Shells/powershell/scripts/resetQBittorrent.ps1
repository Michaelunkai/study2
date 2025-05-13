# qBittorrent Metadata Force Fix Script
# Must be run as administrator

# Ensure running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "Please run this script as Administrator!" -ForegroundColor Red
    Start-Sleep -Seconds 3
    exit
}

# Force kill all qBittorrent and related processes
Get-Process | Where-Object {$_.Name -like "*qbittorrent*" -or $_.Name -like "*torrent*"} | Stop-Process -Force
Start-Sleep -Seconds 2

# Define paths
$qbtPath = "${env:ProgramFiles}\qBittorrent\qbittorrent.exe"
if (-not (Test-Path $qbtPath)) {
    $qbtPath = "${env:ProgramFiles(x86)}\qBittorrent\qbittorrent.exe"
}

# Force clear ALL torrent data and cache
$paths = @(
    "$env:LOCALAPPDATA\qBittorrent\BT_backup",
    "$env:APPDATA\qBittorrent\BT_backup",
    "$env:LOCALAPPDATA\qBittorrent\logs",
    "$env:APPDATA\qBittorrent\logs",
    "$env:TEMP\qBittorrent"
)

foreach ($path in $paths) {
    if (Test-Path $path) {
        Remove-Item -Path $path -Recurse -Force -ErrorAction SilentlyContinue
        New-Item -ItemType Directory -Path $path -Force | Out-Null
    }
}

# Clear specific problematic files
$filesToClear = @(
    "$env:LOCALAPPDATA\qBittorrent\qBittorrent.ini",
    "$env:APPDATA\qBittorrent\qBittorrent.ini",
    "$env:LOCALAPPDATA\qBittorrent\qBittorrent-data.ini",
    "$env:APPDATA\qBittorrent\qBittorrent-data.ini"
)

foreach ($file in $filesToClear) {
    if (Test-Path $file) {
        Remove-Item -Path $file -Force -ErrorAction SilentlyContinue
    }
}

# Force reset network for torrent communication
$networkCommands = @(
    "netsh int ip reset",
    "netsh winsock reset",
    "ipconfig /flushdns",
    "netsh advfirewall reset"
)

foreach ($cmd in $networkCommands) {
    Invoke-Expression $cmd | Out-Null
}

# Kill any existing connections on common torrent ports
$ports = @(6881..6889)
foreach ($port in $ports) {
    $connections = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
    foreach ($conn in $connections) {
        Stop-Process -Id $conn.OwningProcess -Force -ErrorAction SilentlyContinue
    }
}

# Configure Windows Defender exclusions for qBittorrent (if needed)
try {
    Add-MpPreference -ExclusionPath $qbtPath -ErrorAction SilentlyContinue
    Add-MpPreference -ExclusionProcess "qbittorrent.exe" -ErrorAction SilentlyContinue
} catch {
    Write-Host "Could not add Windows Defender exclusions (non-critical)" -ForegroundColor Yellow
}

# Force enable required Windows services
$services = @("BITS", "WSearch", "Browser", "LanmanWorkstation")
foreach ($service in $services) {
    Set-Service -Name $service -StartupType Automatic -ErrorAction SilentlyContinue
    Start-Service -Name $service -ErrorAction SilentlyContinue
}

Write-Host "Preparing to launch qBittorrent with optimal settings..."
Start-Sleep -Seconds 2

# Create optimal settings file
$optimalSettings = @"
[Preferences]
Connection\PortRangeMin=6881
Connection\UPnP=true
Connection\UseUPnP=true
Downloads\DiskWriteCacheSize=512
Downloads\DiskWriteCacheTTL=60
BitTorrent\DHT=true
BitTorrent\DHTPort=6881
BitTorrent\PeX=true
BitTorrent\LSD=true
BitTorrent\MaxConnecs=2000
BitTorrent\MaxConnecsPerTorrent=100
BitTorrent\MaxUploads=50
BitTorrent\MaxUploadsPerTorrent=8
"@

$settingsPath = "$env:LOCALAPPDATA\qBittorrent\qBittorrent.ini"
New-Item -ItemType File -Path $settingsPath -Force
Set-Content -Path $settingsPath -Value $optimalSettings

# Launch qBittorrent with forced settings
Write-Host "Launching qBittorrent..."
Start-Process $qbtPath -ArgumentList "--no-splash"

Write-Host "`nScript complete! qBittorrent has been restarted with optimized settings."
Write-Host "If metadata is still stuck:"
Write-Host "1. Right-click the torrent and choose 'Force recheck'"
Write-Host "2. If that doesn't work, try right-click > 'Force reannounce'"
Write-Host "3. Add more trackers to the torrent through right-click > 'Edit trackers'"

# Wait for user confirmation
Write-Host "`nPress any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
