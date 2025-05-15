# Define target folder and installation path
$downloads = "$env:USERPROFILE\Downloads"
$targetInstallPath = "F:\backup\windowsapps\installed"

# Common silent install flags to try
$silentFlags = @(
    "/S /D=`"$targetInstallPath`"",
    "/silent /dir=`"$targetInstallPath`"",
    "/VERYSILENT /DIR=`"$targetInstallPath`"",
    "/quiet TARGETDIR=`"$targetInstallPath`"",
    "/qn INSTALLDIR=`"$targetInstallPath`""
)

# Get all .exe and .msi files in Downloads
$installers = Get-ChildItem -Path $downloads -Include *.exe, *.msi -Recurse

foreach ($file in $installers) {
    Write-Host "Installing: $($file.FullName)" -ForegroundColor Cyan

    $installed = $false

    foreach ($flag in $silentFlags) {
        try {
            Start-Process -FilePath $file.FullName -ArgumentList $flag -Wait -PassThru -ErrorAction Stop
            Write-Host "Success with flags: $flag" -ForegroundColor Green
            $installed = $true
            break
        } catch {
            Write-Host "Failed with flags: $flag" -ForegroundColor DarkYellow
        }
    }

    if (-not $installed) {
        Write-Host "❌ Could not silently install $($file.Name). Try manual install." -ForegroundColor Red
    }
}

