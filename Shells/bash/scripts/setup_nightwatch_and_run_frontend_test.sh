#!/bin/ 
# Create project directory and navigate to it
mkdir -p nightwatch-test/tests && cd nightwatch-test

# Initialize npm and install Nightwatch
npm init -y && npm install nightwatch

# Initialize Nightwatch and create a basic configuration
npx nightwatch --init

# Create a Python script to generate a test
echo 'with open("tests/sample_test.js", "w") as f:
    f.write("""
module.exports = {
  "Sample Test": function (browser) {
    browser
      .url("http://www.google.com")
      .waitForElementVisible("body", 1000)
      .assert.titleContains("Google")
      .end();
  }
};
""")' > create_nightwatch_test.py

# Run the Python script to create the test
 3 create_nightwatch_test.py

# Update the Nightwatch configuration to point to the 'tests' folder
sed -i "s#src_folders: \[\],#src_folders: \['tests'\],#" nightwatch.conf.js

# Run the test
npx nightwatch
