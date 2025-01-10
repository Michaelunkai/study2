# Create and configure an Ubuntu Container (CT) on Proxmox for Jellyfin server
# This script sets up Jellyfin, enables SSH, and outputs its IP and port.

# Create the container
pct create 106 local:vztmpl/ubuntu-22.04-standard_22.04-1_amd64.tar.zst \
  --hostname jellyfin-server --cores 2 --memory 2048 --swap 512 --net0 name=eth0,bridge=vmbr0,ip=dhcp \
  --rootfs local:8 --features nesting=1 --unprivileged 1

# Set the root password for the container
pct exec 106 -- bash -c "echo 'root:123456' | chpasswd"

# Start the container
pct start 106

# Ensure DNS resolution works by updating the container's DNS configuration
pct exec 106 -- bash -c "
echo 'nameserver 8.8.8.8' > /etc/resolv.conf
echo 'nameserver 8.8.4.4' >> /etc/resolv.conf
"

# Access the container to install Jellyfin and enable SSH
pct exec 106 -- bash -c "
# Update and install prerequisites
apt update && apt upgrade -y
apt install -y curl gnupg software-properties-common openssh-server

# Enable Universe repository for additional dependencies
add-apt-repository universe

# Add Jellyfin repository and GPG key
mkdir -p /etc/apt/keyrings
curl -fsSL https://repo.jellyfin.org/jellyfin_team.gpg.key | gpg --dearmor -o /etc/apt/keyrings/jellyfin.gpg

# Add repository source
export VERSION_CODENAME=\$(grep VERSION_CODENAME /etc/os-release | cut -d= -f2)
cat <<EOF > /etc/apt/sources.list.d/jellyfin.list
deb [signed-by=/etc/apt/keyrings/jellyfin.gpg] https://repo.jellyfin.org/ubuntu \$VERSION_CODENAME main
EOF

# Update package lists and install Jellyfin
apt update
apt install -y jellyfin

# Enable and start Jellyfin as a service
systemctl enable --now jellyfin

# Open firewall ports for Jellyfin
ufw allow 8096/tcp
ufw allow 8920/tcp
ufw reload

# Enable SSH service
systemctl enable --now ssh
"

# Output the IP and port of the Jellyfin server
echo "Jellyfin is available at: http://$(pct exec 106 -- hostname -I | awk '{print $1}'):8096"
