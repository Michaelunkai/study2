#!/usr/bin/env  

# Name: setup_stirlingpdf.sh
# Description: Script to install Stirling-PDF on Ubuntu
# Author: tteck
# License: MIT

# Exit immediately if a command exits with a non-zero status
set -e

# Functions for colored output
function msg_info() {
    echo -e "\033[1;34m[INFO]\033[0m $1"
}

function msg_ok() {
    echo -e "\033[1;32m[OK]\033[0m $1"
}

function msg_error() {
    echo -e "\033[1;31m[ERROR]\033[0m $1"
    exit 1
}

# Check if the script is run as root
if [ "$(id -u)" -ne 0 ]; then
    msg_error "This script must be run as root or with sudo"
fi

# Install dependencies
msg_info "Installing Dependencies (Patience)"
apt-get update && apt-get upgrade -y
apt-get install -y \
    curl \
    sudo \
    mc \
    git \
    automake \
    autoconf \
    libtool \
    libleptonica-dev \
    pkg-config \
    zlib1g-dev \
    make \
    g++ \
    unpaper \
    qpdf \
    poppler-utils
msg_ok "Dependencies installed"

# Install LibreOffice components
msg_info "Installing LibreOffice Components"
apt-get install -y \
    libreoffice-writer \
    libreoffice-calc \
    libreoffice-impress
msg_ok "LibreOffice Components installed"

# Install Python dependencies
msg_info "Installing Python Dependencies"
apt-get install -y \
     3 \
     3-pip
rm -rf /usr/lib/ 3.*/EXTERNALLY-MANAGED
pip3 install \
    uno \
    opencv- -headless \
    unoconv \
    pngquant \
    WeasyPrint
msg_ok "Python Dependencies installed"

# Install Azul Zulu JDK
msg_info "Installing Azul Zulu JDK"
wget -qO /etc/apt/trusted.gpg.d/zulu-repo.asc "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0xB1998361219BD9C9"
wget -q https://cdn.azul.com/zulu/bin/zulu-repo_1.0.0-3_all.deb
dpkg -i zulu-repo_1.0.0-3_all.deb
apt-get update
apt-get -y install zulu17-jdk
msg_ok "Azul Zulu JDK installed"

# Install JBIG2
msg_info "Installing JBIG2"
git clone https://github.com/agl/jbig2enc /opt/jbig2enc
cd /opt/jbig2enc
  ./autogen.sh
  ./configure
make
make install
msg_ok "JBIG2 installed"

# Install Tesseract language packs
msg_info "Installing Tesseract Language Packs (Patience)"
apt-get install -y 'tesseract-ocr-*'
msg_ok "Language Packs installed"

# Install Stirling-PDF
msg_info "Installing Stirling-PDF (Additional Patience)"
RELEASE=$(curl -s https://api.github.com/repos/Stirling-Tools/Stirling-PDF/releases/latest | grep "tag_name" | awk '{print substr($2, 3, length($2)-4) }')
wget -q https://github.com/Stirling-Tools/Stirling-PDF/archive/refs/tags/v$RELEASE.tar.gz
tar -xzf v$RELEASE.tar.gz
cd Stirling-PDF-$RELEASE
chmod +x ./gradlew
./gradlew build
mkdir -p /opt/Stirling-PDF
touch /opt/Stirling-PDF/.env
mv ./build/libs/Stirling-PDF-*.jar /opt/Stirling-PDF/
mv scripts /opt/Stirling-PDF/
ln -s /opt/Stirling-PDF/Stirling-PDF-$RELEASE.jar /opt/Stirling-PDF/Stirling-PDF.jar
ln -s /usr/share/tesseract-ocr/5/tessdata/ /usr/share/tessdata
msg_ok "Stirling-PDF v$RELEASE installed"

# Create systemd service
msg_info "Creating Stirling-PDF Service"
cat <<EOF >/etc/systemd/system/stirlingpdf.service
[Unit]
Description=Stirling-PDF Service
After=syslog.target network.target

[Service]
SuccessExitStatus=143
User=root
Group=root
Type=simple
EnvironmentFile=/opt/Stirling-PDF/.env
WorkingDirectory=/opt/Stirling-PDF
ExecStart=/usr/bin/java -jar Stirling-PDF.jar
ExecStop=/bin/kill -15 %n

[Install]
WantedBy=multi-user.target
EOF

systemctl enable --now stirlingpdf.service
msg_ok "Stirling-PDF service created and started"

# Cleanup
msg_info "Cleaning up"
rm -rf v$RELEASE.tar.gz zulu-repo_1.0.0-3_all.deb
apt-get autoremove -y && apt-get autoclean -y
msg_ok "Cleanup complete"

# Display completion message with URL and tool explanation
msg_info "Stirling-PDF installation complete"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "Stirling-PDF is running and accessible at: http://$IP_ADDRESS:8080"
echo ""
echo "### Stirling-PDF: Document Management Simplified"
echo "A robust tool for document processing, converting, and optimizing PDF files."
