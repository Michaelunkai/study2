#!/bin/ 

# install_glassfish_server_on_ubuntu.sh
# This script installs and configures GlassFish Server on Ubuntu, including dependencies and systemd service.

# Exit immediately if a command exits with a non-zero status
set -e

# Variables
GLASSFISH_VERSION="6.2.5"
GLASSFISH_ZIP="glassfish-${GLASSFISH_VERSION}.zip"
GLASSFISH_DOWNLOAD_URL="https://download.eclipse.org/ee4j/glassfish/glassfish-${GLASSFISH_VERSION}.zip"
INSTALL_DIR="/opt/glassfish6"
USER_NAME="root"
JAVA_HOME_PATH="/usr/lib/jvm/java-11-openjdk-amd64"
ADMIN_PASSWORD="123456"

# Function to install dependencies
install_dependencies() {
    echo "Installing necessary dependencies..."
    sudo apt install -y openjdk-11-jdk unzip wget ufw
    echo "Dependencies installed successfully."
}

# Function to verify Java installation
verify_java() {
    echo "Verifying Java installation..."
    JAVA_VERSION=$(java -version 2>&1 | awk -F '"' '/version/ {print $2}')
    echo "Java version installed: $JAVA_VERSION"
    if [[ "$JAVA_VERSION" < "11" ]]; then
        echo "Java version is less than 11. Exiting."
        exit 1
    fi
    echo "Java installation verified."
}

# Function to download GlassFish
download_glassfish() {
    echo "Downloading GlassFish Server version ${GLASSFISH_VERSION}..."
    wget -O "/tmp/${GLASSFISH_ZIP}" "${GLASSFISH_DOWNLOAD_URL}"
    echo "GlassFish downloaded to /tmp/${GLASSFISH_ZIP}."
}

# Function to extract GlassFish
extract_glassfish() {
    echo "Extracting GlassFish..."
    sudo unzip -o -q "/tmp/${GLASSFISH_ZIP}" -d /opt/
    if [ ! -d "${INSTALL_DIR}" ]; then
        sudo mv "/opt/glassfish6" "${INSTALL_DIR}"
    fi
    sudo chown -R "${USER_NAME}:${USER_NAME}" "${INSTALL_DIR}"
    echo "GlassFish extracted to ${INSTALL_DIR}."
}

# Function to set environment variables
set_environment_variables() {
    echo "Setting environment variables..."
    ENV_FILE="${HOME}/. rc"
    {
        echo ""
        echo "# GlassFish Environment Variables"
        echo "export GLASSFISH_HOME=${INSTALL_DIR}"
        echo "export PATH=\$PATH:\$GLASSFISH_HOME/bin"
    } >> "${ENV_FILE}"
    source "${ENV_FILE}"
    echo "Environment variables set."
}

# Function to start GlassFish server
start_glassfish() {
    echo "Starting GlassFish server..."
    asadmin start-domain || {
        echo "GlassFish server may already be running or the port is in use. Skipping start."
    }
    echo "GlassFish server start attempted."
}

# Function to secure Admin Console
secure_admin_console() {
    echo "Securing GlassFish Admin Console..."
    # Change admin password
    echo "AS_ADMIN_PASSWORD=" > /tmp/pwdfile
    echo "AS_ADMIN_NEWPASSWORD=${ADMIN_PASSWORD}" >> /tmp/pwdfile
    asadmin --user admin --passwordfile /tmp/pwdfile change-admin-password || {
        echo "Failed to change admin password. Skipping this step."
    }
    # Enable secure admin
    echo "AS_ADMIN_PASSWORD=${ADMIN_PASSWORD}" > /tmp/pwdfile
    asadmin --user admin --passwordfile /tmp/pwdfile enable-secure-admin || {
        echo "Failed to enable secure admin. Skipping this step."
    }
    rm /tmp/pwdfile
    # Restart the domain to apply changes
    asadmin restart-domain || {
        echo "Failed to restart domain. Skipping this step."
    }
    echo "Admin Console security configuration attempted."
}

# Function to configure firewall
configure_firewall() {
    echo "Configuring UFW firewall..."
    sudo ufw allow 8080/tcp    # HTTP
    sudo ufw allow 8181/tcp    # HTTPS
    sudo ufw allow 4848/tcp    # Admin Console
    sudo ufw reload
    echo "Firewall configured."
}

# Function to create systemd service
create_systemd_service() {
    echo "Creating systemd service for GlassFish..."
    SERVICE_FILE="/etc/systemd/system/glassfish.service"
    sudo bash -c "cat > ${SERVICE_FILE}" <<EOF
[Unit]
Description=GlassFish Server
After=network.target

[Service]
Type=forking
User=${USER_NAME}
ExecStart=${INSTALL_DIR}/bin/asadmin start-domain
ExecStop=${INSTALL_DIR}/bin/asadmin stop-domain
ExecReload=${INSTALL_DIR}/bin/asadmin restart-domain
Environment=JAVA_HOME=${JAVA_HOME_PATH}
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

    sudo systemctl daemon-reload
    sudo systemctl enable glassfish
    sudo systemctl start glassfish || {
        echo "GlassFish systemd service may already be running or failed to start."
    }
    echo "Systemd service for GlassFish created and started."
}

# Main execution flow
main() {
    install_dependencies
    verify_java
    download_glassfish
    extract_glassfish
    set_environment_variables
    start_glassfish
    secure_admin_console
    configure_firewall
    create_systemd_service
    echo "GlassFish Server installation and configuration completed successfully."
    echo "Access the Admin Console at http://localhost:4848"
    echo "Admin Username: admin"
    echo "Admin Password: ${ADMIN_PASSWORD}"
}

# Run the main function
main
