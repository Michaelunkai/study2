#!/bin/ 

# Create a new directory for the project
mkdir qa_ui_test_project

# Navigate into the project directory
cd qa_ui_test_project

# Initialize a new npm project
npm init -y

# Install required dependencies
npm install selenium-webdriver@4.7.2 chai@4.3.6 http-server@14.1.1

# Create a new file for the login page
echo "<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Login Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        .container {
            width: 300px;
            margin: 50px auto;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        label {
            display: block;
            margin-bottom: 10px;
        }
        input[type='text'], input[type='password'] {
            width: 100%;
            height: 40px;
            margin-bottom: 20px;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        button[type='submit'] {
            width: 100%;
            height: 40px;
            background-color: #4CAF50;
            color: #fff;
            padding: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button[type='submit']:hover {
            background-color: #3e8e41;
        }
    </style>
</head>
<body>
    <div class='container'>
        <h2>Login</h2>
        <form id='login-form'>
            <label for='username'>Username:</label>
            <input type='text' id='username' name='username'><br><br>
            <label for='password'>Password:</label>
            <input type='password' id='password' name='password'><br><br>
            <button type='submit'>Login</button>
        </form>
    </div>

    <script src='script.js'></script>
</body>
</html>" > index.html

# Create a new file for the script
echo "document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('login-form');

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        // Simulate login functionality
        if (username === 'test' && password === 'test') {
            alert('Login successful!');
        } else {
            alert('Invalid username or password');
        }
    });
});" > script.js

# Create a new file for the login test
echo "const { Builder, By, until } = require('selenium-webdriver');
const chai = require('chai');
const chaiAsPromised = require('chai-as-promised');
chai.use(chaiAsPromised);
const expect = chai.expect;

// Describe the test suite
describe('Login Functionality', function () {
    let driver;

    // Before hook to launch the browser
    before(async function () {
        driver = await new Builder().forBrowser('chrome').build();
    });

    // After hook to close the browser
    after(async function () {
        await driver.quit();
    });

    // Test case to verify successful login
    it('should allow user to login with valid credentials', async function () {
        // Navigate to the login page
        await driver.get('http://localhost:8080/index.html');

        // Enter valid username and password
        await driver.findElement(By.id('username')).sendKeys('test');
        await driver.findElement(By.id('password')).sendKeys('test');

        // Click the login button
        await driver.findElement(By. ('button[type=\'submit\']')).click();

        // Wait for the alert to appear
        await driver.wait(until.alertIsPresent());

        // Verify the alert text
        const alertText = await driver.switchTo().alert().getText();
        expect(alertText).to.equal('Login successful!');

        // Accept the alert
        await driver.switchTo().alert().accept();
    });

    // Test case to verify failed login
    it('should display error message for invalid credentials', async function () {
        // Navigate to the login page
        await driver.get('http://localhost:8080/index.html');

        // Enter invalid username and password
        await driver.findElement(By.id('username')).sendKeys('invalid');
        await driver.findElement(By.id('password')).sendKeys('invalid');

        // Click the login button
        await driver.findElement(By. ('button[type=\'submit\']')).click();

        // Wait for the alert to appear
        await driver.wait(until.alertIsPresent());

        // Verify the alert text
        const alertText = await driver.switchTo().alert().getText();
        expect(alertText).to.equal('Invalid username or password');

        // Accept the alert
        await driver.switchTo().alert().accept();
    });
});" > login.test.js

# Install chai-as-promised
npm install chai-as-promised@7.2.4

# Run the http-server
http-server &

# Run the test
node login.test.js
