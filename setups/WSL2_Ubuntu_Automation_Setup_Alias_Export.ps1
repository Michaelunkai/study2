# WSL Ubuntu Setup and Alias Configuration Script

# Unregister and reimport Ubuntu
wsl --unregister ubuntu
wsl --import ubuntu C:\wsl2\ubuntu\ C:\backup\linux\wsl\ubuntu.tar

# Unregister ubuntu2
wsl --unregister ubuntu2

# Run setupWSL2ubuntureplica script
Set-Location C:\study\shells\powershell\scripts
.\setupWSL2ubuntureplica

# Function to run commands in WSL
function Run-WSLCommand {
    param (
        [string]$Command
    )
    wsl -d ubuntu -e bash -c $Command
}

# Copy aliases from Windows to WSL
$aliasContent = Get-Content C:\Users\micha\Desktop\alias.txt -Raw
Run-WSLCommand "echo '$aliasContent' >> ~/.bashrc"
Run-WSLCommand "sudo bash -c ""echo '$aliasContent' >> /root/.bashrc"""

# Source bashrc files and sync them
$wslCommands = @(
    "source ~/.bashrc",
    "source /root/.bashrc",
    "rsync -aP /root/.bashrc /mnt/c/backup/linux/wsl/alias.txt",
    "rsync -aP /root/.bashrc ~/.bashrc",
    "rsync -aP /root/.bashrc /mnt/c/study/shells/bash/.bashrc",
    "sudo cp /root/.bashrc /home/ubuntu/.bashrc",
    "sudo chown ubuntu:ubuntu /home/ubuntu/.bashrc",
    "sudo -u ubuntu bash -c 'source /home/ubuntu/.bashrc'"
)

foreach ($cmd in $wslCommands) {
    Run-WSLCommand $cmd
}

# Export, reimport Ubuntu, and run setupWSL2ubuntureplica again
wsl --export ubuntu C:\backup\linux\wsl\ubuntu.tar
wsl --import ubuntu C:\wsl2\ubuntu\ C:\backup\linux\wsl\ubuntu.tar
wsl --unregister ubuntu2
Set-Location C:\study\shells\powershell\scripts
.\setupWSL2ubuntureplica
wsl -d ubuntu

Write-Host "WSL Ubuntu setup and alias configuration completed."
