# WSL Ubuntu Setup and Alias Configuration Script

# Stop on first error
$ErrorActionPreference = "Stop"

try {
    # Reset WSL instances
    Write-Host "Resetting WSL environment..."
    wsl --unregister ubuntu
    wsl --unregister ubuntu2

    # Import Ubuntu
    Write-Host "Importing Ubuntu..."
    wsl --import ubuntu C:\wsl2\ubuntu\ C:\backup\linux\wsl\ubuntu.tar

    # Run setup replica
    Set-Location C:\study\shells\powershell\scripts
    .\setupWSL2ubuntureplica

    # Create a temporary script to handle the bashrc updates
    $updateScript = @'
#!/bin/bash
# Backup original bashrc
cp /root/.bashrc /root/.bashrc.backup

# Restore original bashrc content
cat /root/.bashrc.backup > /root/.bashrc

# Append alias.txt content to bashrc
cat /mnt/c/Users/micha/Desktop/alias.txt >> /root/.bashrc

# Sync the bashrc files
rsync -aP /root/.bashrc /mnt/c/backup/linux/wsl/alias.txt
rsync -aP /root/.bashrc ~/.bashrc
rsync -aP /root/.bashrc /mnt/c/study/shells/bash/.bashrc
cp /root/.bashrc /home/ubuntu/.bashrc
chown ubuntu:ubuntu /home/ubuntu/.bashrc
'@

    # Save the update script
    $updateScript | Out-File -Encoding utf8 -FilePath "C:\Users\micha\Desktop\update_bashrc.sh"

    # Convert line endings to Unix format
    (Get-Content "C:\Users\micha\Desktop\update_bashrc.sh") | 
        ForEach-Object { $_ -replace "`r`n", "`n" } | 
        Set-Content -NoNewline -Path "C:\Users\micha\Desktop\update_bashrc.sh"

    # Execute the update script in WSL
    Write-Host "Updating bashrc files..."
    wsl -d ubuntu -e sudo bash /mnt/c/Users/micha/Desktop/update_bashrc.sh

    # Clean up
    Remove-Item "C:\Users\micha\Desktop\update_bashrc.sh" -ErrorAction SilentlyContinue

    # Export updated configuration
    Write-Host "Creating backup..."
    wsl --export ubuntu C:\backup\linux\wsl\ubuntu.tar

    # Final setup
    Write-Host "Final setup..."
    wsl --import ubuntu C:\wsl2\ubuntu\ C:\backup\linux\wsl\ubuntu.tar
    
    # Launch WSL
    Write-Host "Setup complete. Launching WSL..."
    wsl -d ubuntu
}
catch {
    Write-Error "An error occurred: $_"
    if (Test-Path "C:\Users\micha\Desktop\update_bashrc.sh") {
        Remove-Item "C:\Users\micha\Desktop\update_bashrc.sh"
    }
    exit 1
}
