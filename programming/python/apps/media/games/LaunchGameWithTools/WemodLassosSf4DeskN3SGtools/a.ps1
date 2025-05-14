<#
    Enhanced Elden Ring Launcher Script
    
    This script:
    1. Launches Elden Ring
    2. Runs the 'rr' function after 10 seconds
    3. After game exit, launches save management tools
#>

############################################################
# 1) User-defined helper functions
############################################################
function desk {
    Write-Host "Running desk function - switching between desktop 1 and 2..." -ForegroundColor Cyan
    if (Test-Path $ahkPath) {
        Push-Location -Path (Split-Path -Path $ahkPath -Parent)
        try {
            & $ahkPath
        } catch {
            Write-Host "Error running AHK script: $_" -ForegroundColor Red
        }
        Pop-Location
    } else {
        Write-Host "AHK script not found at: $ahkPath" -ForegroundColor Red
    }
}

function rlas {
    Write-Host "Running rlas function - restarting Process Lasso..." -ForegroundColor Cyan
    try {
        Stop-Process -Name "processlasso" -Force -ErrorAction SilentlyContinue
        Write-Host "Process Lasso stopped." -ForegroundColor Green
    } catch {
        Write-Host "Process Lasso was not running or couldn't be stopped: $_" -ForegroundColor Yellow
    }
    
    if (Test-Path $plPath) {
        try {
            Start-Process -FilePath $plPath
            Write-Host "Process Lasso started." -ForegroundColor Green
        } catch {
            Write-Host "Failed to start Process Lasso: $_" -ForegroundColor Red
        }
    } else {
        Write-Host "Process Lasso not found at: $plPath" -ForegroundColor Red
    }
}

function superf4 {
    Write-Host "Running superf4 function - starting SuperF4..." -ForegroundColor Cyan
    $exeWD = Split-Path -Path $superf4Path -Parent
    
    if (Test-Path $superf4Path) {
        try {
            Start-Process -FilePath $superf4Path -WorkingDirectory $exeWD
            Write-Host "SuperF4 started." -ForegroundColor Green
        } catch {
            Write-Host "Failed to start SuperF4: $_" -ForegroundColor Red
        }
    } else {
        Write-Host "SuperF4 not found at: $superf4Path" -ForegroundColor Red
    }
}

function rmod {
    Write-Host "Running rmod function - restarting WeMod..." -ForegroundColor Cyan
    try {
        Stop-Process -Name "WeMod" -Force -ErrorAction SilentlyContinue
        Write-Host "WeMod stopped." -ForegroundColor Green
    } catch {
        Write-Host "WeMod was not running or couldn't be stopped: $_" -ForegroundColor Yellow
    }
    
    if (Test-Path $wemodPath) {
        try {
            Start-Process -FilePath $wemodPath
            Write-Host "WeMod started." -ForegroundColor Green
        } catch {
            Write-Host "Failed to start WeMod: $_" -ForegroundColor Red
        }
    } else {
        Write-Host "WeMod not found at: $wemodPath" -ForegroundColor Red
    }
}

function sg {
    Write-Host "Running sg function..." -ForegroundColor Cyan
    # Add your sg function implementation here if needed
}

function rr {
    Write-Host "Running rr function sequence..." -ForegroundColor Green
    desk
    rlas
    superf4
    rmod
}

############################################################
# 2) Path configuration - Edit these paths as needed
############################################################
# Game paths
$gamePath        = "F:\games\eldenrings\Game\eldenring.exe"      # Actual game executable
$launcherPath    = "F:\games\eldenrings\Game\Language Selector.exe"  # Game launcher

# Save management tools
$savestatePath   = "F:\backup\windowsapps\installed\SaveState\SaveState.exe"       # SaveState tool
$ludusaviPath    = "F:\backup\windowsapps\installed\ludusavi\ludusavi.exe"         # Ludusavi backup tool
$gsmPath         = "F:\backup\windowsapps\installed\gameSaveManager\gs_mngr_3.exe" # Game Save Manager

# Helper application paths
$ahkPath         = "F:\study\Platforms\windows\autohotkey\switchBetweenDesktop1And2.ahk"
$plPath          = "F:\backup\windowsapps\installed\Process Lasso\ProcessLasso.exe"
$superf4Path     = "F:\backup\windowsapps\installed\SuperF4\SuperF4.exe"
$wemodPath       = "C:\Users\micha\AppData\Local\WeMod\WeMod.exe"

############################################################
# 3) Launch Elden Ring and prepare for monitoring
############################################################
Write-Host "Launching Elden Ring..." -ForegroundColor Yellow
$erProcess = Start-Process -FilePath $launcherPath `
                          -WorkingDirectory (Split-Path -Path $launcherPath -Parent) `
                          -PassThru

############################################################
# 4) Wait 10 seconds, then run pre-game helpers (rr)
############################################################
Write-Host "Waiting 10 seconds before running pre-game helpers..." -ForegroundColor Yellow
Start-Sleep -Seconds 10
Write-Host "Running pre-game helper functions..." -ForegroundColor Yellow
rr

############################################################
# 5) Wait for main game process to exit
############################################################
# The launcher might start the actual game process, so we need to find and monitor that
Write-Host "Monitoring for game exit..." -ForegroundColor Yellow

# Wait loop - checks every 15 seconds if the game is still running
try {
    # First wait for launcher process to complete if needed
    if ($null -ne $erProcess -and !$erProcess.HasExited) {
        $erProcess | Wait-Process -Timeout 300 -ErrorAction SilentlyContinue
    }
    
    # Then monitor for the actual game process
    $monitoring = $true
    while ($monitoring) {
        $gameProcesses = Get-Process -Name "eldenring", "start_protected_game" -ErrorAction SilentlyContinue
        
        if ($gameProcesses.Count -eq 0) {
            $monitoring = $false
        } else {
            Start-Sleep -Seconds 15
        }
    }
}
catch {
    Write-Host "Error while monitoring game process: $_" -ForegroundColor Red
}
finally {
    ########################################################
    # 6) Post-game helpers: run sg function and backup apps
    ########################################################
    Write-Host "Game closed. Running post-game helpers and backup apps..." -ForegroundColor Yellow
    
    # Run sg function
    sg
    
    # Launch backup applications
    Write-Host "Launching save management tools..." -ForegroundColor Green
    
    # Launch each tool with error handling
    foreach ($tool in @($savestatePath, $ludusaviPath, $gsmPath)) {
        if (Test-Path $tool) {
            try {
                Start-Process -FilePath $tool -WindowStyle Normal
                Write-Host "Started: $(Split-Path $tool -Leaf)" -ForegroundColor Green
            } catch {
                Write-Host "Failed to start: $(Split-Path $tool -Leaf) - $_" -ForegroundColor Red
            }
        } else {
            Write-Host "Tool not found: $(Split-Path $tool -Leaf)" -ForegroundColor Yellow
        }
    }
    
    Write-Host "All operations completed successfully!" -ForegroundColor Green
}

# Exit the script cleanly
exit 0
