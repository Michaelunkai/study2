# Define paths
$chromeDriverPath = "$env:USERPROFILE\Downloads\chromedriver.exe"
$ ScriptPath = "C:\study\Credentials\linkedin\LinkedIn-Easy-Apply-Bot\easybot3.py"
$updatedPythonScriptPath = "C:\study\Credentials\linkedin\LinkedIn-Easy-Apply-Bot\easybot3_updated.py"

# Function to download the latest ChromeDriver
function Download-LatestChromeDriver {
    $latestVersion = Invoke-RestMethod -Uri "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
    $downloadUrl = "https://chromedriver.storage.googleapis.com/$latestVersion/chromedriver_win32.zip"
    $zipPath = "$env:USERPROFILE\Downloads\chromedriver_win32.zip"

    # Download the latest ChromeDriver
    Invoke-WebRequest -Uri $downloadUrl -OutFile $zipPath
    # Expand the archive and overwrite existing files
    Expand-Archive -Path $zipPath -DestinationPath "$env:USERPROFILE\Downloads" -Force
    # Remove the downloaded zip file
    Remove-Item $zipPath
}

# Download the latest ChromeDriver
Download-LatestChromeDriver

# Set environment variables for ChromeDriver
[System.Environment]::SetEnvironmentVariable("PATH", "$env:PATH;$env:USERPROFILE\Downloads")

# Create a new Python script with updated Chrome options
$pythonScriptContent = Get-Content $pythonScriptPath
$updatedPythonScriptContent = @"
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--headless")  # Uncomment this line if you want to run in headless mode

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

"@
$updatedPythonScriptContent += $ ScriptContent

# Save the updated script
$updatedPythonScriptContent | Out-File -FilePath $updatedPythonScriptPath -Encoding utf8

Write-Host "ChromeDriver updated and environment variables set. Your Python script has been updated and saved as 'easybot3_updated.py'."

