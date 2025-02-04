# Import Selenium module
Import-Module Selenium

# Set Bumble URL
$bumbleUrl = "https://bumble.com"

# Set the path to GeckoDriver executable
$geckoDriverPath = "C:\Users\micha\Downloads"

# Create Firefox options object
$firefoxOptions = New-Object OpenQA.Selenium.Firefox.FirefoxOptions

# Start a new browser session with GeckoDriver
$driver = New-Object OpenQA.Selenium.Firefox.FirefoxDriver($geckoDriverPath, $firefoxOptions)

# Navigate to Bumble website
$driver.Navigate().GoToUrl($bumbleUrl)

# Find the Log in with Facebook button and click it
$facebookSignInButton = $driver.FindElementByXPath("//span[text()='Continue with Facebook']")
$facebookSignInButton.Click()

# Wait for the Facebook login page to load
Start-Sleep -Seconds 5  # Adjust this wait time as needed

# Switch to the Facebook login iframe
$iframe = $driver.FindElementByTagName("iframe")
$driver.SwitchTo().Frame($iframe)

# Find and enter the email address
$emailField = $driver.FindElementById("email")
$emailField.SendKeys($email)

# Find and enter the password
$passwordField = $driver.FindElementById("pass")
$passwordField.SendKeys($password)

# Find and click the Login button
$loginButton = $driver.FindElementById("loginbutton")
$loginButton.Click()

# Wait for the Facebook login process to complete
Start-Sleep -Seconds 10  # Adjust this wait time as needed

# Switch back to the default content
$driver.SwitchTo().DefaultContent()

# Wait for Bumble to load
Start-Sleep -Seconds 10  # Adjust this wait time as needed

# Loop for swiping right
while ($true) {
    # Find the body element and send a right arrow key press
    $driver.FindElementByTagName("body").SendKeys([OpenQA.Selenium.Keys]::Right)

    # Wait for the next potential match to load
    Start-Sleep -Seconds 2  # Adjust this wait time as needed
}

# Close the browser
$driver.Quit()
