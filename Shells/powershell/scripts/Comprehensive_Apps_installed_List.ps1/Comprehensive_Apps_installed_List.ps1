# List applications installed via traditional installers (64-bit)
$traditionalApps64 = Get-ItemProperty -Path "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*" |
Select-Object DisplayName, DisplayVersion, Publisher, InstallDate |
Where-Object { $_.DisplayName } |
Sort-Object DisplayName |
Format-Table -AutoSize

# List 32-bit applications on a 64-bit system
$traditionalApps32 = Get-ItemProperty -Path "HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*" |
Select-Object DisplayName, DisplayVersion, Publisher, InstallDate |
Where-Object { $_.DisplayName } |
Sort-Object DisplayName |
Format-Table -AutoSize

# List all Microsoft Store apps including enterprise or specific configurations
$storeApps = Get-AppxPackage -AllUsers |
Select-Object Name, PackageFullName |
Sort-Object Name |
Format-Table -AutoSize

# List applications installed with Chocolatey
$chocoApps = choco list --local-only |
ForEach-Object {
    $package = $_ -split '\|'
    [PSCustomObject]@{
        Name    = $package[0]
        Version = $package[1]
    }
} | Sort-Object Name | Format-Table -AutoSize

# List applications installed with Scoop
$scoopApps = @()
if (Get-Command scoop -ErrorAction SilentlyContinue) {
    $scoopApps = scoop list |
    ForEach-Object {
        $package = $_ -split '\s+'
        [PSCustomObject]@{
            Name    = $package[0]
            Version = $package[1]
        }
    } | Sort-Object Name | Format-Table -AutoSize
}

# List applications installed with Ninite (requires manual path, example assumes default Ninite log location)
$niniteApps = @()
$niniteLogPath = "$env:PROGRAMDATA\Ninite\InstalledApps.txt"
if (Test-Path $niniteLogPath) {
    $niniteApps = Get-Content $niniteLogPath |
    ForEach-Object {
        [PSCustomObject]@{
            Name = $_
        }
    } | Sort-Object Name | Format-Table -AutoSize
}

# List portable applications by scanning common directories (example for Desktop and Downloads)
$portableApps = Get-ChildItem -Path "$env:USERPROFILE\Desktop", "$env:USERPROFILE\Downloads" -Recurse -Include *.exe |
Select-Object FullName |
Sort-Object FullName |
Format-Table -AutoSize

# List applications in the "Add or Remove Programs" list
$addRemovePrograms = Get-WmiObject -Query "SELECT * FROM Win32_Product" |
Select-Object Name, Version, Vendor |
Sort-Object Name |
Format-Table -AutoSize

# Output all results
Write-Output "Traditional Applications (64-bit):"
$traditionalApps64
Write-Output "`nTraditional Applications (32-bit):"
$traditionalApps32
Write-Output "`nMicrosoft Store Applications:"
$storeApps
Write-Output "`nChocolatey Applications:"
$chocoApps
Write-Output "`nScoop Applications:"
$scoopApps
Write-Output "`nNinite Applications:"
$niniteApps
Write-Output "`nPortable Applications:"
$portableApps
Write-Output "`nApplications from 'Add or Remove Programs':"
$addRemovePrograms
