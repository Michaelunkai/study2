# Define installation path
$installPath = "C:\backup\windosapps\installed\speedtest-cli"

# Download the Speedtest CLI ZIP file
Write-Host "Downloading Speedtest CLI..."
iwr -Uri "https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-win64.zip" -OutFile "$env:TEMP\ookla-speedtest.zip"

# Create installation directory
Write-Host "Creating installation directory..."
mkdir $installPath -Force

# Extract the ZIP file to the installation directory
Write-Host "Extracting files..."
Expand-Archive -Path "$env:TEMP\ookla-speedtest.zip" -DestinationPath $installPath

# Add the installation directory to the system PATH
Write-Host "Updating system PATH..."
[Environment]::SetEnvironmentVariable("Path", "$($env:Path);$installPath", [EnvironmentVariableTarget]::Machine)
$env:Path = [Environment]::GetEnvironmentVariable("Path", [EnvironmentVariableTarget]::Machine)

# Run Speedtest CLI to confirm installation
Write-Host "Running Speedtest CLI..."
cd $installPath
speedtest
