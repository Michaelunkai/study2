[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$InstallerUri = "https://desktop.docker.com/win/stable/Docker%20Desktop%20Installer.exe"
$InstallerPath = ".\DockerDesktopInstaller.exe"

Invoke-WebRequest -Uri $InstallerUri -OutFile $InstallerPath -UseBasicParsing
Start-Process -Wait -FilePath $InstallerPath
Remove-Item -Path $InstallerPath

