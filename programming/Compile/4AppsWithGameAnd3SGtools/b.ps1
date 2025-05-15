<#
    Enhanced Elden Ring Launcher Script with Global Hotkeys (Ctrl+S = sused, Ctrl+R = resed)
#>

##########################
# 1) Suspend/Resume Tools
##########################
function sused {
    & "F:\backup\windowsapps\installed\PSTools\pssuspend.exe" eldenring.exe
}
function resed {
    & "F:\backup\windowsapps\installed\PSTools\pssuspend.exe" -r eldenring.exe
}

##########################
# 2) AutoHotkey Keybindings
##########################
$ahkTemp = "$env:TEMP\hotkeys_suspend_resume.ahk"
Set-Content -Path $ahkTemp -Value @"
^s::Run, powershell.exe -WindowStyle Hidden -Command "sused"
^r::Run, powershell.exe -WindowStyle Hidden -Command "resed"
"@
Start-Process -FilePath "C:\Program Files\AutoHotkey\AutoHotkey.exe" -ArgumentList "`"$ahkTemp`""

##########################
# 3) Support Functions
##########################
function desk {
    if (Test-Path $ahkPath) { & $ahkPath }
}
function rlas {
    Stop-Process -Name "processlasso" -Force -ErrorAction SilentlyContinue
    if (Test-Path $plPath) { Start-Process -FilePath $plPath }
}
function superf4 {
    if (Test-Path $superf4Path) {
        Start-Process -FilePath $superf4Path -WorkingDirectory (Split-Path $superf4Path -Parent)
    }
}
function rmod {
    Stop-Process -Name "WeMod" -Force -ErrorAction SilentlyContinue
    if (Test-Path $wemodPath) { Start-Process -FilePath $wemodPath }
}
function rr {
    desk; rlas; superf4; rmod
}
function sg {
    # Optional post-game logic placeholder
}

##########################
# 4) Paths
##########################
$gamePath      = "F:\games\eldenrings\Game\eldenring.exe"
$launcherPath  = "F:\games\eldenrings\Game\Language Selector.exe"
$savestatePath = "F:\backup\windowsapps\installed\SaveState\SaveState.exe"
$ludusaviPath  = "F:\backup\windowsapps\installed\ludusavi\ludusavi.exe"
$gsmPath       = "F:\backup\windowsapps\installed\gameSaveManager\gs_mngr_3.exe"
$ahkPath       = "F:\study\Platforms\windows\autohotkey\switchBetweenDesktop1And2.ahk"
$plPath        = "F:\backup\windowsapps\installed\Process Lasso\ProcessLasso.exe"
$superf4Path   = "F:\backup\windowsapps\installed\SuperF4\SuperF4.exe"
$wemodPath     = "C:\Users\micha\AppData\Local\WeMod\WeMod.exe"

##########################
# 5) Launch Game
##########################
Write-Host "Launching Elden Ring..." -ForegroundColor Yellow
$erProcess = Start-Process -FilePath $launcherPath `
    -WorkingDirectory (Split-Path $launcherPath -Parent) `
    -PassThru

##########################
# 6) Wait & Prepare
##########################
Start-Sleep -Seconds 10
rr

##########################
# 7) Monitor Game
##########################
try {
    if ($erProcess -and !$erProcess.HasExited) {
        $erProcess | Wait-Process -Timeout 300 -ErrorAction SilentlyContinue
    }

    while ($true) {
        $gameProcesses = Get-Process -Name "eldenring", "start_protected_game" -ErrorAction SilentlyContinue
        if ($gameProcesses.Count -eq 0) { break }
        Start-Sleep -Seconds 15
    }
}
catch {
    Write-Host "Error monitoring game: $_" -ForegroundColor Red
}
finally {
    sg
    foreach ($tool in @($savestatePath, $ludusaviPath, $gsmPath)) {
        if (Test-Path $tool) {
            Start-Process -FilePath $tool
        } else {
            Write-Host "Missing: $tool" -ForegroundColor Yellow
        }
    }
    Write-Host "Finished!" -ForegroundColor Green
}
exit 0
