# Create a PowerShell script that will install winget in the sandbox
$installScript = @"
# Create a temporary directory
New-Item -Path "C:\Temp" -ItemType Directory -Force | Out-Null
Set-Location -Path "C:\Temp"

Write-Host "Installing dependencies for winget..." -ForegroundColor Yellow

# Download and install Microsoft.UI.Xaml
Write-Host "Downloading Microsoft.UI.Xaml..."
Invoke-WebRequest -Uri "https://aka.ms/Microsoft.UI.Xaml.2.7.zip" -OutFile ".\Microsoft.UI.Xaml.2.7.zip"
Expand-Archive -Path ".\Microsoft.UI.Xaml.2.7.zip" -DestinationPath ".\xaml" -Force
Add-AppxPackage ".\xaml\tools\AppX\x64\Release\Microsoft.UI.Xaml.2.7.appx"

# Download and install Microsoft.VCLibs
Write-Host "Downloading VCLibs..."
Invoke-WebRequest -Uri "https://aka.ms/Microsoft.VCLibs.x64.14.00.Desktop.appx" -OutFile ".\Microsoft.VCLibs.x64.14.00.Desktop.appx"
Add-AppxPackage ".\Microsoft.VCLibs.x64.14.00.Desktop.appx"

# Download and install winget
Write-Host "Downloading and installing winget..."
$latestWingetMsixBundleUri = "https://github.com/microsoft/winget-cli/releases/latest/download/Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle"
Invoke-WebRequest -Uri $latestWingetMsixBundleUri -OutFile ".\winget.msixbundle"
Add-AppxPackage -Path ".\winget.msixbundle"

# Test if winget is working
Write-Host "Testing winget installation..." -ForegroundColor Green
winget --version

# Clean up
Remove-Item -Path ".\Microsoft.UI.Xaml.2.7.zip" -Force -ErrorAction SilentlyContinue
Remove-Item -Path ".\Microsoft.VCLibs.x64.14.00.Desktop.appx" -Force -ErrorAction SilentlyContinue
Remove-Item -Path ".\winget.msixbundle" -Force -ErrorAction SilentlyContinue

Write-Host "Installation complete. PowerShell window will remain open." -ForegroundColor Green
"@

# Save the install script to a file
$installScriptPath = "$env:TEMP\InstallWinget.ps1"
$installScript | Out-File -FilePath $installScriptPath -Encoding UTF8

# Define the content of the Sandbox configuration file
$wsbContent = @"
<Configuration>
  <MappedFolders>
    <MappedFolder>
      <HostFolder>C:\backup</HostFolder>
      <SandboxFolder>C:\backup</SandboxFolder>
      <ReadOnly>true</ReadOnly>
    </MappedFolder>
    <MappedFolder>
      <HostFolder>C:\study</HostFolder>
      <SandboxFolder>C:\study</SandboxFolder>
      <ReadOnly>true</ReadOnly>
    </MappedFolder>
    <MappedFolder>
      <HostFolder>C:\wsl2</HostFolder>
      <SandboxFolder>C:\wsl2</SandboxFolder>
      <ReadOnly>true</ReadOnly>
    </MappedFolder>
    <MappedFolder>
      <HostFolder>C:\games</HostFolder>
      <SandboxFolder>C:\games</SandboxFolder>
      <ReadOnly>true</ReadOnly>
    </MappedFolder>
    <MappedFolder>
      <HostFolder>$env:TEMP</HostFolder>
      <SandboxFolder>C:\HostTemp</SandboxFolder>
      <ReadOnly>false</ReadOnly>
    </MappedFolder>
  </MappedFolders>
  <LogonCommand>
    <Command>powershell.exe -ExecutionPolicy Bypass -NoExit -Command "Start-Process powershell.exe -ArgumentList '-ExecutionPolicy Bypass -NoExit -File C:\HostTemp\InstallWinget.ps1' -Verb RunAs"</Command>
  </LogonCommand>
  <MemoryInMB>4096</MemoryInMB>
  <NetworkingEnabled>true</NetworkingEnabled>
  <AudioInput>false</AudioInput>
  <VideoInput>false</VideoInput>
  <ProtectedClient>true</ProtectedClient>
  <ClipboardRedirection>true</ClipboardRedirection>
</Configuration>
"@

# Save the configuration to a temporary .wsb file
$wsbPath = "$env:TEMP\SandboxConfig.wsb"
$wsbContent | Out-File -FilePath $wsbPath -Encoding UTF8

# Launch Windows Sandbox with the configuration file
Start-Process -FilePath "C:\Windows\System32\WindowsSandbox.exe" -ArgumentList $wsbPath
