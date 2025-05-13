#!/bin/ 

# Variables
EASY_RSA_DIR=~/openvpn-ca
SERVER_IP="0.0.0.0"
CLIENT_NAME="client1"
NGINX_CONFIG="/etc/nginx/sites-available/openvpn"

# Update system and install required packages
sudo apt-get update
sudo apt-get install -y openvpn easy-rsa nginx

# Check if the Easy-RSA directory already exists
if [ -d "$EASY_RSA_DIR" ]; then
    echo "$EASY_RSA_DIR exists. Aborting."
    exit 1
fi

# Set up the Public Key Infrastructure (PKI)
make-cadir $EASY_RSA_DIR
cd $EASY_RSA_DIR

# Configure vars for Easy-RSA
sed -i 's/export KEY_COUNTRY=".*"/export KEY_COUNTRY="US"/' vars
sed -i 's/export KEY_PROVINCE=".*"/export KEY_PROVINCE="CA"/' vars
sed -i 's/export KEY_CITY=".*"/export KEY_CITY="SanFrancisco"/' vars
sed -i 's/export KEY_ORG=".*"/export KEY_ORG="MyOrg"/' vars
sed -i 's/export KEY_EMAIL=".*"/export KEY_EMAIL="email@example.com"/' vars
sed -i 's/export KEY_OU=".*"/export KEY_OU="MyOrgUnit"/' vars
sed -i 's/export KEY_NAME=".*"/export KEY_NAME="server"/' vars

# Initialize the PKI and build the CA
./easyrsa init-pki
./easyrsa build-ca nopass

# Generate the server certificate and key
./easyrsa gen-req server nopass
./easyrsa sign-req server server

# Generate Diffie-Hellman parameters
./easyrsa gen-dh

# Generate a shared TLS key
openvpn --genkey secret ta.key

# Generate client certificates
./easyrsa gen-req $CLIENT_NAME nopass
./easyrsa sign-req client $CLIENT_NAME

# Copy server certificates and keys to OpenVPN directory
sudo cp pki/private/server.key /etc/openvpn/
sudo cp pki/issued/server.crt /etc/openvpn/
sudo cp pki/ca.crt /etc/openvpn/
sudo cp pki/dh.pem /etc/openvpn/dh2048.pem
sudo cp ta.key /etc/openvpn/

# Create OpenVPN server configuration
sudo bash -c "cat > /etc/openvpn/server.conf << EOF
port 1194
proto udp
dev tun
ca ca.crt
cert server.crt
key server.key
dh dh2048.pem
tls-auth ta.key 0
server 10.8.0.0 255.255.255.0
ifconfig-pool-persist ipp.txt
keepalive 10 120
cipher AES-256-CBC
user nobody
group nogroup
persist-key
persist-tun
status openvpn-status.log
verb 3
local $SERVER_IP
EOF"

# Enable IP forwarding
sudo sed -i 's/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/' /etc/sysctl.conf
sudo sysctl -p

# Start and enable OpenVPN service
sudo systemctl start openvpn@server
sudo systemctl enable openvpn@server

# Check if OpenVPN service started successfully
if systemctl status openvpn@server | grep -q "active (running)"; then
    echo "OpenVPN service started successfully."
else
    echo "OpenVPN service failed to start. Check the logs for details."
    exit 1
fi

# Generate client configuration files
mkdir -p ~/client-configs/keys
cp pki/ca.crt ~/client-configs/keys/
cp ta.key ~/client-configs/keys/
cp pki/issued/$CLIENT_NAME.crt ~/client-configs/keys/
cp pki/private/$CLIENT_NAME.key ~/client-configs/keys/

cat > ~/client-configs/base.conf << EOF
client
dev tun
proto udp
remote $SERVER_IP 1194
resolv-retry infinite
nobind
user nobody
group nogroup
persist-key
persist-tun
ca ca.crt
cert $CLIENT_NAME.crt
key $CLIENT_NAME.key
tls-auth ta.key 1
cipher AES-256-CBC
verb 3
EOF

cd ~/client-configs
tar -czvf $CLIENT_NAME.tar.gz base.conf keys/

# Optional: Configure Nginx for SSL termination
if [ -f "$NGINX_CONFIG" ]; then
    echo "$NGINX_CONFIG already exists. Skipping Nginx configuration."
else
    sudo bash -c "cat > $NGINX_CONFIG << EOF
server {
    listen 443 ssl;
    server_name your_domain_or_ip;

    ssl_certificate /etc/ssl/certs/your_cert.crt;
    ssl_certificate_key /etc/ssl/private/your_key.key;

    location / {
        proxy_pass https://127.0.0.1:1194;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF"

    sudo ln -s $NGINX_CONFIG /etc/nginx/sites-enabled/
    sudo systemctl restart nginx

    # Check if Nginx service started successfully
    if systemctl status nginx | grep -q "active (running)"; then
        echo "Nginx service started successfully."
    else
        echo "Nginx service failed to start. Check the logs for details."
        exit 1
    fi
fi

echo "SSL VPN setup is complete. The client configuration files are available in ~/client-configs."
