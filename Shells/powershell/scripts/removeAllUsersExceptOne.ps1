# Set the username and password
$Username = "micha"
$Password = ConvertTo-SecureString "123456" -AsPlainText -Force

# Get all local users
$Users = Get-LocalUser

# Remove all users except "micha"
foreach ($User in $Users) {
    if ($User.Name -ne $Username -and $User.Name -ne "Administrator") {
        Remove-LocalUser -Name $User.Name -ErrorAction SilentlyContinue
    }
}

# Ensure "micha" exists, if not create it
if (-not (Get-LocalUser -Name $Username -ErrorAction SilentlyContinue)) {
    New-LocalUser -Name $Username -Password $Password -FullName "Micha" -Description "Primary User Account"
}

# Add "micha" to Administrators group
Add-LocalGroupMember -Group "Administrators" -Member $Username -ErrorAction SilentlyContinue

# Disable built-in Administrator account for security
Disable-LocalUser -Name "Administrator"

# Force automatic login for "micha"
$RegPath = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"
Set-ItemProperty -Path $RegPath -Name "AutoAdminLogon" -Value "1" -Type String
Set-ItemProperty -Path $RegPath -Name "DefaultUserName" -Value $Username -Type String
Set-ItemProperty -Path $RegPath -Name "DefaultPassword" -Value "123456" -Type String

Write-Host "Cleanup completed. Only 'micha' remains with full admin rights and auto-login enabled."
