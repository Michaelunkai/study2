# Continuous Monitoring of Windows Resources (CPU and Memory)
while ($true) {
    # Get current CPU usage percentage
    $cpuUsage = Get-WmiObject Win32_PerfFormattedData_PerfOS_Processor | Where-Object { $_.Name -eq "_Total" } | Select-Object -ExpandProperty PercentProcessorTime
    Write-Host "CPU Usage: $($cpuUsage)%"

    # Get current memory usage
    $memory = Get-WmiObject Win32_OperatingSystem
    $totalMemory = $memory.TotalVisibleMemorySize / 1MB
    $freeMemory = $memory.FreePhysicalMemory / 1MB
    $usedMemory = $totalMemory - $freeMemory
    $memoryUsagePercentage = ($usedMemory / $totalMemory) * 100
    Write-Host "Memory Usage: $($memoryUsagePercentage)%"

    # Get detailed memory usage by process
    $processes = Get-Process | Sort-Object -Property WS -Descending | Select-Object -First 5
    Write-Host "Top 5 Processes by Memory Usage:"
    foreach ($process in $processes) {
        $memoryUsageMB = $process.WorkingSet / 1MB
        Write-Host "    $($process.Name): $($memoryUsageMB) MB"
    }

    # Get detailed CPU usage by process
    $processes = Get-WmiObject Win32_PerfFormattedData_PerfProc_Process | Sort-Object -Property PercentProcessorTime -Descending | Select-Object -First 5
    Write-Host "Top 5 Processes by CPU Usage:"
    foreach ($process in $processes) {
        $cpuUsagePercent = $process.PercentProcessorTime
        Write-Host "    $($process.Name): $($cpuUsagePercent)%"
    }

    # Delay for 5 seconds before checking again
    Start-Sleep -Seconds 5
}
