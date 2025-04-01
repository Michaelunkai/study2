#Requires AutoHotkey v2.0+
#SingleInstance Force

; ------------------------- CONFIGURATION -------------------------
global GameEXE      := "eldenring.exe"           ; Your game's EXE name
global GamePath     := "C:\Games\EldenRing"      ; Game folder (for skipping intros)
global HighPerfGUID := "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"  ; High-Performance power plan GUID

; List of helper apps to launch:
; • WeMod
; • Process Lasso
; • The folder "C:\games" (opens visibly in File Explorer)
; • JoyToKey
; • GHelper
global appsToLaunch := [
    "C:\Users\micha\AppData\Local\WeMod\WeMod.exe",
    "C:\Program Files\Process Lasso\ProcessLassoLauncher.exe",
    "C:\games",  ; Opens visibly in File Explorer
    "C:\Program Files (x86)\JoyToKey\JoyToKey.exe",
    "C:\Users\micha\AppData\Local\Microsoft\WinGet\Packages\seerge.g-helper_Microsoft.Winget.Source_8wekyb3d8bbwe\GHelper.exe"
]

; ------------------------- GLOBAL VARIABLES -------------------------
global isGaming     := false
global launchedPIDs := []    ; Array to hold PIDs of launched helper apps

; ------------------------- HOTKEY TOGGLE -------------------------
^!g::ToggleGamingMode()  ; Press Ctrl+Alt+G to toggle Gaming Mode

ToggleGamingMode() {
    global isGaming
    isGaming := !isGaming
    if isGaming {
        MsgBox "🚀 Gaming Mode ACTIVATED"
        OptimizeSystemForGaming()
    } else {
        MsgBox "🔧 Gaming Mode DEACTIVATED – Restoring system..."
        RestoreSystemAfterGaming()
    }
}

; ------------------------- OPTIMIZE SYSTEM FOR GAMING -------------------------
OptimizeSystemForGaming() {
    ; 1. Switch to High-Performance Power Plan
    Run("powercfg /setactive " HighPerfGUID, , "Hide")
    
    ; 2. Terminate background processes that may drain resources
    blocked := ["explorer.exe", "OneDrive.exe", "YourPhone.exe", "SearchApp.exe", "RuntimeBroker.exe", "StartMenuExperienceHost.exe", "SteamWebHelper.exe"]
    for proc in blocked {
        if ProcessExist(proc)
            ProcessClose(proc)
    }
    
    ; 3. Disable Windows Defender real‑time scanning
    Run("powershell -command Set-MpPreference -DisableRealtimeMonitoring $true", , "Hide")
    
    ; 4. Disable Windows notifications
    RegWrite(2, "REG_DWORD", "HKCU\Software\Microsoft\Windows\CurrentVersion\Notifications\Settings", "NOC_GLOBAL_SETTING_TOASTS_ENABLED")
    
    ; 5. Prevent sleep/monitor timeouts
    Run("powercfg /change standby-timeout-ac 0", , "Hide")
    Run("powercfg /change monitor-timeout-ac 0", , "Hide")
    
    ; 6. Free up RAM by triggering idle tasks
    Run('cmd.exe /c echo | "%windir%\system32\rundll32.exe" advapi32.dll,ProcessIdleTasks', , "Hide")
    
    ; 7. Launch each helper app and store its PID
    for appPath in appsToLaunch {
        LaunchApp(appPath)
    }
    
    ; 8. Start a timer to monitor and boost the game process (by GameEXE)
    SetTimer(() => BoostGamePerformance(GameEXE), 3000)
    
    ; 9. Skip intro videos in the game folder by renaming them
    SkipIntroVideos(GamePath)
}

; ------------------------- RESTORE SYSTEM AFTER GAMING -------------------------
RestoreSystemAfterGaming() {
    ; 1. Restart Explorer (if it was terminated)
    Run("explorer.exe", , "Hide")
    
    ; 2. Switch back to the Balanced power plan
    Run("powercfg /setactive SCHEME_BALANCED", , "Hide")
    
    ; 3. Re-enable Windows Defender real‑time scanning
    Run("powershell -command Set-MpPreference -DisableRealtimeMonitoring $false", , "Hide")
    
    ; 4. Re-enable Windows notifications
    RegWrite(1, "REG_DWORD", "HKCU\Software\Microsoft\Windows\CurrentVersion\Notifications\Settings", "NOC_GLOBAL_SETTING_TOASTS_ENABLED")
    
    ; 5. Close all launched helper apps
    for pid in launchedPIDs {
        ProcessClose(pid)
    }
    launchedPIDs := []    ; Reset the array
}

; ------------------------- BOOST GAME PERFORMANCE -------------------------
BoostGamePerformance(gameExe) {
    pid := ProcessExist(gameExe)
    if pid {
        ; Boost game process: set high priority (priority level 128)
        Run('cmd /c wmic process where ProcessId=' pid ' CALL setpriority 128', , "Hide")
        ; Set CPU affinity (example: cores 0,2,4,6; bitmask 0x55)
        handle := DllCall("OpenProcess", "UInt", 0x1F0FFF, "Int", 0, "UInt", pid, "Ptr")
        DllCall("SetProcessAffinityMask", "Ptr", handle, "UInt", 0x55)
        ; Stop further timer invocations (once boosted)
        SetTimer(() => BoostGamePerformance(gameExe), 0)
    }
}

; ------------------------- SKIP INTRO VIDEOS -------------------------
SkipIntroVideos(path) {
    try {
        Loop Files path "\*intro*.mp4", "FR" {
            FileMove(A_LoopFileFullPath, A_LoopFileFullPath ".bak", true)
        }
        Loop Files path "\*logo*.bik", "FR" {
            FileMove(A_LoopFileFullPath, A_LoopFileFullPath ".bak", true)
        }
    }
}

; ------------------------- LAUNCH HELPER APPS -------------------------
LaunchApp(appPath) {
    global launchedPIDs
    ; If the path is a folder, open it visibly in File Explorer.
    if FileExist(appPath) = "D" {
        pid := Run('explorer.exe "' appPath '"')
    } else {
        ; Launch the application hidden
        pid := Run('"' appPath '"', , "Hide")
    }
    launchedPIDs.Push(pid)
}
