#!/bin/ 

# Install required packages and clone the BeEF repository
sudo apt install -y ruby ruby-dev git
git clone https://github.com/beefproject/beef
cd beef

# Update the default username and password in the config file
sed -i 's/user: "beef"/user: "test"/' config.yaml
sed -i 's/passwd: "beef"/passwd: "test"/' config.yaml

# Install BeEF and its dependencies
yes | sudo ./install
sudo gem install bundler
bundle install

# Start BeEF in the background
nohup sudo ./beef > /dev/null 2>&1 &

# Wait for BeEF to start
sleep 10

# Open Chrome with the authentication URL
cmd.exe /c start chrome http://localhost:3000/ui/authentication

# Echo the username and password
echo "Username: beef"
echo "Password: test"
