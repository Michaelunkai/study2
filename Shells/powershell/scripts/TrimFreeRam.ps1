# Copy EmptyStandbyList.exe to System32 (Requires Admin)
$sourcePath = "C:\backup\windowsapps\install\EmptyStandbyList.exe"
$destinationPath = "C:\Windows\System32\EmptyStandbyList.exe"

if (Test-Path $sourcePath) {
    Copy-Item -Path $sourcePath -Destination $destinationPath -Force
    Write-Host "✅ EmptyStandbyList.exe copied to System32" -ForegroundColor Green
} else {
    Write-Host "❌ ERROR: Source file not found! ($sourcePath)" -ForegroundColor Red
    exit
}

# Start RAM Cleanup Loop
while ($true) {
    $before = (Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory
    Start-Process -FilePath $destinationPath -ArgumentList workingsets -NoNewWindow -Wait
    Start-Sleep 2
    $after = (Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory
    $freed = [math]::Round(($after - $before) / 1024, 2)
    Write-Host "💾 Freed: $freed MB" -ForegroundColor Cyan
    Start-Sleep 10  # Adjust cleanup frequency
}
