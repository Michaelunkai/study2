# Define source and destination paths
$sourcePath = "C:\"
$destinationPath = "F:\Backup"

# Get total used space of the C drive
$usedSpace = (Get-PSDrive -Name "C").Used

# Convert used space to gigabytes
$usedSpaceGB = [math]::Round($usedSpace / 1GB, 2)

# Create a timestamp for the backup folder
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"

# Append used space to the backup folder name
$backupFolderName = "Backup_${timestamp}_UsedSpace${usedSpaceGB}GB"
$backupFolder = Join-Path -Path $destinationPath -ChildPath $backupFolderName

# Create the backup folder
New-Item -Path $backupFolder -ItemType Directory

# Copy files from source to destination
Copy-Item -Path $sourcePath\* -Destination $backupFolder -Recurse
