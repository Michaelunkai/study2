# Download Docker Desktop Installer
Invoke-WebRequest -Uri https://desktop.docker.com/win/stable/Docker%20Desktop%20Installer.exe -OutFile DockerDesktopInstaller.exe

# Install Docker Desktop
Start-Process -Wait -FilePath .\DockerDesktopInstaller.exe
