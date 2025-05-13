#!/bin/bash

# Exit on any error
set -e

echo "Starting comprehensive Docker purge and fresh installation process..."

# Function to check if command exists
command_exists() {
    command -v "$@" > /dev/null 2>&1
}

# Function to check if running as root
check_root() {
    if [ "$(id -u)" != "0" ]; then
        echo "This script must be run as root" 1>&2
        exit 1
    fi
}

check_root

echo "Step 0: Installing required system utilities..."
apt-get update
apt-get install -y \
    iproute2 \
    net-tools \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    gnupg-agent \
    software-properties-common \
    lsb-release

echo "Step 1: Stopping all Docker services and containers..."
if command_exists docker; then
    # Stop all running containers
    docker kill $(docker ps -q) 2>/dev/null || true
    # Stop all Docker services
    systemctl stop docker.service || true
    systemctl stop docker.socket || true
    systemctl stop containerd.service || true
fi

echo "Step 2: Removing ALL Docker-related packages..."
# Extended list of packages to remove
for pkg in docker.io docker-doc docker-compose docker-compose-v2 docker-ce docker-ce-cli docker-ce-rootless-extras docker-engine docker-registry docker-scan-plugin containerd docker-buildx runc podman-docker moby-engine moby-cli moby-buildx moby-compose moby-containerd moby-runc nvidia-docker2 nvidia-container-runtime; do
    apt-get remove -y $pkg 2>/dev/null || true
    apt-get purge -y $pkg 2>/dev/null || true
done

echo "Step 3: Purging ALL Docker-related configurations and data..."
# Remove packages and dependencies
apt-get autoremove -y
apt-get autoclean -y

# Remove all Docker-related directories and files
directories=(
    "/var/lib/docker"
    "/var/lib/containerd"
    "/etc/docker"
    "/etc/containerd"
    "/var/run/docker"
    "/var/run/containerd"
    "/usr/local/bin/docker*"
    "/usr/local/bin/containerd*"
    "/usr/bin/docker*"
    "/usr/bin/containerd*"
    "/opt/containerd"
    "/home/*/.docker"
    "/root/.docker"
    "/var/log/docker"
    "/var/log/containerd"
    "/etc/apparmor.d/docker"
    "/etc/apt/sources.list.d/docker*.list"
    "/etc/apt/sources.list.d/nvidia-docker*.list"
    "/etc/systemd/system/docker*"
    "/etc/systemd/system/containerd*"
    "/etc/init.d/docker"
    "/etc/default/docker"
    "/usr/share/docker*"
    "/usr/share/containerd*"
    "/usr/libexec/docker"
    "/var/cache/apt/archives/docker*"
    "/var/cache/apt/archives/containerd*"
)

for dir in "${directories[@]}"; do
    rm -rf $dir 2>/dev/null || true
done

# Remove Docker group
groupdel docker 2>/dev/null || true

# Remove all Docker-related network interfaces
ip link show | grep -i docker | awk -F': ' '{print $2}' | xargs -r -l ip link delete 2>/dev/null || true
ip link show | grep -i br- | awk -F': ' '{print $2}' | xargs -r -l ip link delete 2>/dev/null || true
ip link show | grep -i cni | awk -F': ' '{print $2}' | xargs -r -l ip link delete 2>/dev/null || true

# Clean up systemd
systemctl daemon-reload
systemctl reset-failed

echo "Step 4: Removing Docker GPG keys..."
rm -f /usr/share/keyrings/docker-archive-keyring.gpg
rm -f /usr/share/keyrings/docker.gpg
rm -f /etc/apt/keyrings/docker.gpg
apt-key del "9DC8 5822 9FC7 DD38 854A E2D8 8D81 803C 0EBF CD88" 2>/dev/null || true

echo "Step 5: Setting up fresh Docker installation..."
# Install prerequisites
apt-get update
apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    gnupg-agent \
    software-properties-common \
    lsb-release

# Add Docker's official GPG key
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

# Set up the stable repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null

echo "Step 6: Installing Docker Engine and ALL related packages..."
apt-get update
apt-get install -y \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    docker-buildx-plugin \
    docker-compose-plugin \
    docker-ce-rootless-extras

echo "Step 7: Setting up Docker daemon with optimal configuration..."
mkdir -p /etc/docker
cat > /etc/docker/daemon.json <<EOF
{
    "log-driver": "json-file",
    "log-opts": {
        "max-size": "10m",
        "max-file": "3"
    },
    "storage-driver": "overlay2",
    "dns": ["8.8.8.8", "8.8.4.4"],
    "max-concurrent-downloads": 10,
    "max-concurrent-uploads": 10,
    "experimental": true,
    "features": {
        "buildkit": true
    }
}
EOF

echo "Step 8: Setting up system for Docker..."
# Create required directories with proper permissions
mkdir -p /var/lib/docker
mkdir -p /var/run/docker
mkdir -p /usr/share/docker

# Set up system groups
groupadd --force docker

# Add current user to docker group if SUDO_USER exists
if [ -n "$SUDO_USER" ]; then
    usermod -aG docker "$SUDO_USER" || true
fi

# Set proper permissions
chown root:docker /var/run/docker
chmod 2775 /var/run/docker

echo "Step 9: Starting and enabling Docker services..."
systemctl enable containerd
systemctl start containerd
systemctl enable docker
systemctl start docker

echo "Step 10: Installing Docker Compose v2..."
COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep 'tag_name' | cut -d '"' -f 4)
mkdir -p ~/.docker/cli-plugins/
curl -SL "https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-linux-$(uname -m)" -o ~/.docker/cli-plugins/docker-compose
chmod +x ~/.docker/cli-plugins/docker-compose

echo "Step 11: Setting up Docker BuildX..."
# Remove any existing buildx installations
rm -rf ~/.docker/buildx

# Install buildx plugin
mkdir -p ~/.docker/cli-plugins
curl -SL "https://github.com/docker/buildx/releases/latest/download/buildx-v0.12.1.linux-amd64" -o ~/.docker/cli-plugins/docker-buildx
chmod +x ~/.docker/cli-plugins/docker-buildx

# Initialize buildx with a new builder instance
docker buildx create --name mybuilder --use || true
docker buildx inspect --bootstrap

echo "Step 12: Verifying installation..."
echo "Docker Engine version:"
docker --version
echo "Docker Compose version:"
docker compose version
echo "Docker Buildx version:"
docker buildx version
echo "Testing Docker installation:"
docker run --rm hello-world

echo "Step 13: Setting up WSL2 specific configurations..."
if [ -n "$SUDO_USER" ]; then
    WSL_CONF_DIR="/home/$SUDO_USER/.wslconfig"
    cat > "$WSL_CONF_DIR" <<EOF
[wsl2]
memory=8GB
processors=4
swap=4GB
kernelCommandLine=systemd=true
EOF
    chown "$SUDO_USER:$SUDO_USER" "$WSL_CONF_DIR"
fi

echo "Installation complete! Please log out and log back in for group changes to take effect."

cat << "EOF"

Post-Installation Steps:
-----------------------
1. Restart your WSL2 instance:
   wsl --shutdown
   wsl

2. Verify Docker is running:
   docker ps

3. Test Docker thoroughly:
   docker run -d -p 80:80 nginx
   curl localhost:80

Common Docker Commands:
----------------------
- List containers: docker ps -a
- List images: docker images
- Pull image: docker pull <image>
- Build image: docker build -t <name> .
- Run container: docker run <image>
- Stop container: docker stop <container>
- Remove container: docker rm <container>
- Remove image: docker rmi <image>

For any issues:
--------------
1. Check Docker service: systemctl status docker
2. Check Docker logs: journalctl -u docker
3. Verify group membership: groups $USER
4. Check Docker info: docker info

EOF
