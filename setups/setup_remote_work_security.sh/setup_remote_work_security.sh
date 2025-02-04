#!/bin/ 

# Update system packages
sudo apt update && sudo apt upgrade -y

# Install UFW
sudo apt install -y ufw

# Allow OpenSSH through UFW and enable UFW
sudo ufw allow OpenSSH
sudo ufw --force enable

# Install Fail2Ban
sudo apt install -y fail2ban

# Configure Fail2Ban
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local

sudo tee -a /etc/fail2ban/jail.local > /dev/null <<EOL

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 5

EOL

# Start and enable Fail2Ban service
sudo systemctl start fail2ban
sudo systemctl enable fail2ban

# Install OpenSSH server
sudo apt install -y openssh-server

# Configure SSH for security
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config

# Restart SSH service to apply changes
sudo systemctl restart ssh

# Generate SSH key pair if not already exists
if [ ! -f ~/.ssh/id_rsa ]; then
    ssh-keygen -t rsa -b 4096 -N "" -f ~/.ssh/id_rsa
fi

# Install ClamAV antivirus
sudo apt install -y clamav clamav-daemon

# Update ClamAV database
sudo freshclam

# Run ClamAV scan on the home directory
sudo clamscan -r /home

# Notify user of completion
echo "Security setup completed successfully."

# Restart services to ensure all settings take effect
sudo systemctl restart fail2ban
sudo systemctl restart ufw
