# Get temperature information for CPU
$cpuTemp = Get-WmiObject -Namespace "root\OpenHardwareMonitor" -Class "Sensor" | Where-Object {$_.SensorType -eq "Temperature" -and $_.Name -like "*CPU*"} | Select-Object -ExpandProperty Value

# Get temperature information for GPU
$gpuTemp = Get-WmiObject -Namespace "root\OpenHardwareMonitor" -Class "Sensor" | Where-Object {$_.SensorType -eq "Temperature" -and $_.Name -like "*GPU*"} | Select-Object -ExpandProperty Value

# Display results
Write-Host "CPU Temperature: $cpuTemp °C"
Write-Host "GPU Temperature: $gpuTemp °C"
