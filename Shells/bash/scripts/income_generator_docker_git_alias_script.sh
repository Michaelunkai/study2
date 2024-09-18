#!/bin/bash

# Step 1: Remove the existing repository if it already exists
if [ -d "/root/.income-generator" ]; then
    rm -rf /root/.income-generator
fi

# Step 2: Clone the "Income Generator" repository to /root/.income-generator
git clone --depth=1 https://github.com/XternA/income-generator.git /root/.income-generator

# Step 3: Automatically generate default .env configuration file with placeholders
cat <<EOL > /root/.income-generator/.env
HONEYGAIN_EMAIL=your_email@example.com
HONEYGAIN_PASSWORD=your_password
EARNAPP_EMAIL=your_email@example.com
EARNAPP_PASSWORD=your_password
PEER2PROFIT_EMAIL=your_email@example.com
PEER2PROFIT_PASSWORD=your_password
TRAFFMONETIZER_EMAIL=your_email@example.com
TRAFFMONETIZER_PASSWORD=your_password
PAWNS_EMAIL=your_email@example.com
PAWNS_PASSWORD=your_password
REPOCKET_EMAIL=your_email@example.com
REPOCKET_PASSWORD=your_password
PACKETSTREAM_EMAIL=your_email@example.com
PACKETSTREAM_PASSWORD=your_password
PROXYRACK_EMAIL=your_email@example.com
PROXYRACK_PASSWORD=your_password
PROXYLITE_EMAIL=your_email@example.com
PROXYLITE_PASSWORD=your_password
EARNFM_EMAIL=your_email@example.com
EARNFM_PASSWORD=your_password
SPIDE_EMAIL=your_email@example.com
SPIDE_PASSWORD=your_password
SPEEDSHARE_EMAIL=your_email@example.com
SPEEDSHARE_PASSWORD=your_password
GRASS_EMAIL=your_email@example.com
GRASS_PASSWORD=your_password
MYSTNODE_EMAIL=your_email@example.com
MYSTNODE_PASSWORD=your_password
BITPING_EMAIL=your_email@example.com
BITPING_PASSWORD=your_password
GAGANODE_EMAIL=your_email@example.com
GAGANODE_PASSWORD=your_password
NODEPAY_EMAIL=your_email@example.com
NODEPAY_PASSWORD=your_password
BEARSHARE_EMAIL=your_email@example.com
BEARSHARE_PASSWORD=your_password
EOL

# Step 4: Register alias for global access
# Ensure the alias is added to root's shell configuration
echo "alias igm=\"sh -c 'cd /root/.income-generator; sh start.sh \\\"\\\$@\\\"' --\"" >> /root/."${SHELL##*/}rc"
source /root/."${SHELL##*/}rc"

# Step 5: Run the tool automatically
igm --silent

# Step 6: Automatically skip the credential prompts by preloading the .env configuration
echo "Tool is running with pre-configured credentials."

# Step 7: Check Docker status
sudo systemctl status docker
