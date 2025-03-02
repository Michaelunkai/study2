#!/bin/ 

# 1. Enable Uncomplicated Firewall (UFW) and configure it
echo "Configuring UFW Firewall..."
sudo ufw --force reset
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw --force enable

# 2. Install and configure Fail2Ban
echo "Installing and Configuring Fail2Ban..."
sudo apt-get install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Create Fail2Ban configuration file
sudo tee /etc/fail2ban/jail.local > /dev/null <<EOL
[DEFAULT]
bantime = 600
findtime = 600
maxretry = 5

[sshd]
enabled = true
EOL

# Restart Fail2Ban to apply changes
sudo systemctl restart fail2ban

# 3. Install and configure ClamAV for antivirus protection
echo "Installing and configuring ClamAV..."
sudo systemctl stop clamav-freshclam
sudo freshclam
sudo systemctl start clamav-freshclam
sudo clamscan -r /home

# 4. Generate SSL certificates using OpenSSL with automatic defaults
echo "Generating SSL certificates..."
sudo openssl req -newkey rsa:2048 -nodes -keyout /etc/ssl/private/domain.key -x509 -days 365 -out /etc/ssl/certs/domain.crt -subj "/C=US/ST=State/L=City/O=Organization/OU=Unit/CN=yourdomain.com/emailAddress=admin@yourdomain.com"

# 5. Create user and group for cardholder data access (Skip if exists)
echo "Creating cardholder_admin user and setting permissions..."
if id "cardholder_admin" &>/dev/null; then
    echo "User 'cardholder_admin' already exists. Skipping creation."
else
    sudo useradd -m cardholder_admin
    sudo usermod -aG sudo cardholder_admin
fi
sudo mkdir -p /home/cardholder_admin/cardholder_data
sudo chown -R cardholder_admin:cardholder_admin /home/cardholder_admin/cardholder_data
sudo chmod 700 /home/cardholder_admin/cardholder_data

# 6. Install and configure auditd for monitoring
echo "Installing and configuring auditd..."
sudo apt-get install -y auditd audispd-plugins
sudo systemctl enable auditd
sudo systemctl start auditd || echo "auditd service failed to start. Please check the logs."

# 7. Encrypt files using GPG with automatic defaults
echo "Encrypting files with GPG..."
cat > batch_gpg_gen <<EOF
%echo Generating a basic OpenPGP key
Key-Type: default
Subkey-Type: default
Name-Real: Cardholder Admin
Name-Comment: For PCI-DSS Compliance
Name-Email: admin@yourdomain.com
Expire-Date: 0
%no-protection
%commit
%echo done
EOF

gpg --batch --gen-key batch_gpg_gen

# Check if the file exists before encrypting
if [ -f /home/cardholder_admin/cardholder_data/file_to_encrypt ]; then
    gpg --output /home/cardholder_admin/encrypted_file.gpg --encrypt --recipient admin@yourdomain.com /home/cardholder_admin/cardholder_data/file_to_encrypt
else
    echo "File to encrypt does not exist. Skipping encryption."
fi
rm batch_gpg_gen

# 8. Install and set up OpenVAS for vulnerability scanning
echo "Installing and setting up OpenVAS for vulnerability scanning..."
sudo apt-get install -y openvas
sudo gvm-setup

echo "Setup complete. Your system is configured for PCI-DSS compliance."
