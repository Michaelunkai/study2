# Check RAM Usage
Get-WmiObject Win32_ComputerSystem | Select-Object TotalPhysicalMemory

# Check if the system recognizes all the RAM
Get-CimInstance Win32_PhysicalMemory | Measure-Object Capacity -Sum

# Display Memory Information
$memory = Get-CimInstance Win32_PhysicalMemory
$totalMemory = $memory | Measure-Object -Property Capacity -Sum | Select-Object -ExpandProperty Sum
$usableMemory = (Get-WmiObject Win32_OperatingSystem).TotalVisibleMemorySize
$totalMemoryGB = [math]::Round($totalMemory / 1GB, 2)
$usableMemoryGB = [math]::Round($usableMemory / 1MB, 2)

Write-Output "Total Installed RAM: $totalMemoryGB GB"
Write-Output "Usable RAM: $usableMemoryGB GB"

if ($totalMemoryGB -eq 32 -and $usableMemoryGB -lt $totalMemoryGB) {
    Write-Output "Your system is not using all installed RAM. Please check BIOS settings or memory configuration."
} else {
    Write-Output "Your system is using all installed RAM."
}

# Provide Guidance on Enabling Full RAM Usage
Write-Output "`nTo ensure your system is using all installed RAM, follow these steps:"
Write-Output "1. Check if the RAM sticks are properly installed."
Write-Output "2. Ensure your BIOS is updated to the latest version."
Write-Output "3. In BIOS, verify that 'Memory Remapping' is enabled (if available)."
Write-Output "4. Check if your operating system version supports more than 32 GB RAM (e.g., Windows 10 Pro)."
