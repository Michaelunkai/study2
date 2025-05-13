# WSL Ubuntu Setup and Alias Configuration Script

# SECURITY WARNING: Hardcoding passwords is extremely risky and not recommended for production use.
$password = "123456"

# Function to run commands in WSL with password
function Run-WSLCommand {
    param (
        [string]$Command
    )
    echo $password | wsl -d ubuntu -e sudo -S bash -c $Command
}

# Unregister and reimport Ubuntu
wsl --unregister ubuntu
wsl --import ubuntu C:\wsl2\ubuntu\ C:\backup\linux\wsl\ubuntu.tar

# Unregister ubuntu2
wsl --unregister ubuntu2

# Run setupWSL2ubuntureplica script
Set-Location C:\study\shells\ \scripts
.\setupWSL2ubuntureplica

# Copy aliases from Windows to WSL and replace existing aliases with the same name
$aliasContent = Get-Content C:\Users\micha\Desktop\alias.txt -Raw
$aliasLines = $aliasContent -split "`n"

# Replace aliases in /root/.bashrc
foreach ($alias in $aliasLines) {
    $aliasName = $alias -replace 'alias ', '' -replace '=.*', ''
    $replaceCommand = "sed -i '/alias $aliasName=/d' /root/.bashrc && echo '$alias' >> /root/.bashrc"
    Run-WSLCommand $replaceCommand
}

# Source bashrc files and sync them
$wslCommands = @(
    "source ~/. rc",
    "source /root/. rc",
    "rsync -aP /root/.bashrc /mnt/c/backup/linux/wsl/alias.txt",
    "rsync -aP /root/.bashrc ~/.bashrc",
    "rsync -aP /root/.bashrc /mnt/c/study/shells/bash/.bashrc",
    "cp /root/. rc /home/ubuntu/. rc",
    "chown ubuntu:ubuntu /home/ubuntu/. rc",
    "su - ubuntu -c 'source /home/ubuntu/.bashrc'"
)

foreach ($cmd in $wslCommands) {
    Run-WSLCommand $cmd
}

# Export, reimport Ubuntu, and run setupWSL2ubuntureplica again
wsl --export ubuntu C:\backup\linux\wsl\ubuntu.tar
wsl --import ubuntu C:\wsl2\ubuntu\ C:\backup\linux\wsl\ubuntu.tar
wsl --unregister ubuntu2

Set-Location C:\study\shells\ \scripts
.\setupWSL2ubuntureplica

# Launch WSL Ubuntu
wsl -d ubuntu -e bash -c "cd /mnt/c/backup/windowsapps && docker build -t michadockermisha/backup:windowsapps . && docker push michadockermisha/backup:windowsapps && cd /mnt/c/study && docker build -t michadockermisha/backup:study . && docker push michadockermisha/backup:study && cd /mnt/c/backup/linux/wsl && docker build -t michadockermisha/backup:wsl . && docker push michadockermisha/backup:wsl && exec bash"

Write-Host "WSL Ubuntu setup and alias configuration completed."
