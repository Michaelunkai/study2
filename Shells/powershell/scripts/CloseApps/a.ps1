# Step 1: Kill known process names
$appsToKill = @(
    "gs_mngr_3",             # GameSave Manager
    "ludusavi",
    "savestate",
    "superf4",
    "wemod",
    "everything",
    "SamsungNotesSysTray",
    "todoist",
    "autohotkey",
    "AutoHotkeyUX",
    "Taskmgr",
    "RadeonSoftware",        # AMD Software: Adrenalin
    "RadeonSettings",
    "AMDRSServ",
    "AMDRSSvc",
    "AMDRSSrcExt",
    "AMDRSSysTray",
    "cncmd",
    "atieclxx",
    "atiesrxx",
    "ADLX",
    "AMDCrashDefender",
    "eldenring"              # Elden Ring
)

foreach ($app in $appsToKill) {
    Get-Process -Name $app -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
}

# Step 2: Kill AutoHotkey processes (scripts or compiled)
Get-Process | Where-Object {
    $_.Path -like "*AutoHotkey*" -or
    $_.Name -like "*ahk*" -or
    $_.MainWindowTitle -like "*AutoHotkey*"
} | Stop-Process -Force -ErrorAction SilentlyContinue

# Step 3: Kill AMD background processes by path/title if they slipped through
Get-Process | Where-Object {
    $_.Path -like "*AMD*" -or
    $_.Name -like "*Radeon*" -or
    $_.Name -like "*AMDRS*" -or
    $_.Name -like "*ADLX*" -or
    $_.MainWindowTitle -like "*Radeon*" -or
    $_.Path -like "*Adrenalin*"
} | Stop-Process -Force -ErrorAction SilentlyContinue

# Step 4: Kill Samsung Notes only (smart filter)
Get-CimInstance Win32_Process | Where-Object {
    $_.Name -eq "BackgroundTaskHost.exe" -and $_.CommandLine -match "SamsungNotes"
} | ForEach-Object {
    Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
}
