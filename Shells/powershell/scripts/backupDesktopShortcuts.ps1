# Define paths
$desktopPath = [System.Environment]::GetFolderPath("Desktop")
$backupDir = "C:\Users\micha\Downloads\Desktop_Backup"
$backupFilePath = "C:\Users\micha\Downloads\desktop_shortcuts_backup.txt"

# Function to create a directory with proper permissions
function Ensure-Directory {
    param (
        [string]$Path
    )
    
    if (-Not (Test-Path -Path $Path)) {
        try {
            New-Item -ItemType Directory -Path $Path -Force
        } catch {
            Write-Error "Failed to create directory $Path. Error: $_"
            exit 1
        }
    }
}

# Ensure the backup directory exists
Ensure-Directory -Path $backupDir

# Backup shortcuts and their target paths
try {
    Get-ChildItem -Path $desktopPath -Filter *.lnk | ForEach-Object {
        $shortcut = $_.FullName
        $wshShell = New-Object -ComObject WScript.Shell
        $shortcutObject = $wshShell.CreateShortcut($shortcut)
        $targetPath = $shortcutObject.TargetPath
        "$shortcut|$targetPath" >> $backupFilePath
    }
} catch {
    Write-Error "Failed to backup shortcuts. Error: $_"
    exit 1
}

# Copy all desktop items to the backup directory
try {
    Copy-Item -Path "$desktopPath\*" -Destination $backupDir -Recurse -Force
} catch {
    Write-Error "Failed to copy desktop items to backup directory. Error: $_"
    exit 1
}

Write-Output "Backup completed successfully!"
