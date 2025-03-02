# Stop the WSL instance if it's running
wsl --terminate ubuntu

# Export the existing Ubuntu distro to a backup file
$backupPath = "C:\wsl2\ubuntu-backup.tar"
$installPath = "C:\wsl2\ubuntu2"

# Create the directory structure if it doesn't exist
New-Item -ItemType Directory -Force -Path "C:\wsl2"
New-Item -ItemType Directory -Force -Path $installPath

# Export the existing distro
wsl --export ubuntu $backupPath

# Import the backup as a new distro named ubuntu2
wsl --import ubuntu2 $installPath $backupPath

# Clean up the backup file
Remove-Item $backupPath

# Verify the new distro is listed
wsl --list --verbose
