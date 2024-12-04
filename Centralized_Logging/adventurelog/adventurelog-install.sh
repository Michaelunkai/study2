#!/usr/bin/env bash

# ------------------------------------------------------------------------------
# Script to Install AdventureLog on Ubuntu 22.04 WSL2
# Adapted for WSL2 by ChatGPT
# ------------------------------------------------------------------------------

set -euo pipefail

# ------------------------------- Configuration -------------------------------

# Variables
REPO_URL="https://github.com/seanmorley15/AdventureLog"
ADVENTURELOG_DIR="/opt/adventurelog"
CREDS_FILE="$HOME/adventurelog.creds"
VERSION_FILE="/opt/adventurelog_version.txt"

# ------------------------------- Functions -----------------------------------

# Function to display informational messages
msg_info() {
    echo -e "\e[34m[INFO]\e[0m $1"
}

# Function to display success messages
msg_ok() {
    echo -e "\e[32m[SUCCESS]\e[0m $1"
}

# Function to install dependencies
install_dependencies() {
    msg_info "Installing Dependencies"
    sudo apt-get update
    sudo apt-get install -y \
      gpg \
      curl \
      sudo \
      mc \
      gdal-bin \
      libgdal-dev \
      git \
      python3-venv \
      python3-pip \
      unzip \
      wget \
      openssl
    msg_ok "Installed Dependencies"
}

# Function to set up Node.js repository and install Node.js
setup_nodejs() {
    msg_info "Setting up Node.js Repository"
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    msg_ok "Set up Node.js Repository"

    msg_info "Installing Node.js and pnpm"
    sudo apt-get install -y nodejs
    sudo npm install -g pnpm
    msg_ok "Installed Node.js and pnpm"
}

# Function to set up PostgreSQL repository and install PostgreSQL
setup_postgresql() {
    msg_info "Setting up PostgreSQL Repository"
    curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg
    echo "deb https://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list > /dev/null
    sudo apt-get update
    msg_ok "Set up PostgreSQL Repository"

    msg_info "Installing PostgreSQL and PostGIS"
    sudo apt-get install -y postgresql-16 postgresql-16-postgis
    msg_ok "Installed PostgreSQL and PostGIS"
}

# Function to set up PostgreSQL database and user
setup_database() {
    msg_info "Setting up PostgreSQL Database"

    DB_NAME="adventurelog_db"
    DB_USER="adventurelog_user"
    DB_PASS="$(openssl rand -base64 18 | tr -dc 'a-zA-Z0-9' | cut -c1-13)"
    SECRET_KEY="$(openssl rand -base64 32 | tr -dc 'a-zA-Z0-9' | cut -c1-32)"

    sudo -u postgres psql -c "CREATE ROLE $DB_USER WITH LOGIN PASSWORD '$DB_PASS';"
    sudo -u postgres psql -c "CREATE DATABASE $DB_NAME WITH OWNER $DB_USER ENCODING 'UTF8' TEMPLATE template0;"
    sudo -u postgres psql -d "$DB_NAME" -c "CREATE EXTENSION IF NOT EXISTS postgis;"
    sudo -u postgres psql -c "ALTER ROLE $DB_USER SET client_encoding TO 'utf8';"
    sudo -u postgres psql -c "ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';"
    sudo -u postgres psql -c "ALTER ROLE $DB_USER SET timezone TO 'UTC';"

    {
        echo "AdventureLog-Credentials"
        echo "AdventureLog Database User: $DB_USER"
        echo "AdventureLog Database Password: $DB_PASS"
        echo "AdventureLog Database Name: $DB_NAME"
        echo "AdventureLog Secret: $SECRET_KEY"
    } >> "$CREDS_FILE"

    msg_ok "Set up PostgreSQL Database"
}

# Function to install AdventureLog
install_adventurelog() {
    msg_info "Installing AdventureLog (Patience)"

    DJANGO_ADMIN_USER="djangoadmin"
    DJANGO_ADMIN_PASS="$(openssl rand -base64 18 | tr -dc 'a-zA-Z0-9' | cut -c1-13)"
    LOCAL_IP="$(hostname -I | awk '{print $1}')"

    sudo mkdir -p /opt
    sudo chown "$USER":"$USER" /opt

    cd /opt

    RELEASE=$(curl -s https://api.github.com/repos/seanmorley15/AdventureLog/releases/latest | grep "tag_name" | awk '{print substr($2, 3, length($2)-4)}')
    wget -q "https://github.com/seanmorley15/AdventureLog/archive/refs/tags/v${RELEASE}.zip"
    unzip -q "v${RELEASE}.zip"
    mv "AdventureLog-${RELEASE}" "$ADVENTURELOG_DIR"
    rm "v${RELEASE}.zip"

    # Backend Configuration
    cat <<EOF > "$ADVENTURELOG_DIR/backend/server/.env"
PGHOST='localhost'
PGDATABASE='${DB_NAME}'
PGUSER='${DB_USER}'
PGPASSWORD='${DB_PASS}'
SECRET_KEY='${SECRET_KEY}'
PUBLIC_URL='http://${LOCAL_IP}:8000'
DEBUG=True
FRONTEND_URL='http://${LOCAL_IP}:3000'
CSRF_TRUSTED_ORIGINS='http://127.0.0.1:3000,http://localhost:3000,http://${LOCAL_IP}:3000'
DJANGO_ADMIN_USERNAME='${DJANGO_ADMIN_USER}'
DJANGO_ADMIN_PASSWORD='${DJANGO_ADMIN_PASS}'
DISABLE_REGISTRATION=False
# EMAIL_BACKEND='email'
# EMAIL_HOST='smtp.gmail.com'
# EMAIL_USE_TLS=False
# EMAIL_PORT=587
# EMAIL_USE_SSL=True
# EMAIL_HOST_USER='user'
# EMAIL_HOST_PASSWORD='password'
# DEFAULT_FROM_EMAIL='user@example.com'
EOF

    # Backend Setup
    cd "$ADVENTURELOG_DIR/backend/server"
    mkdir -p media
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    python manage.py collectstatic --noinput
    python manage.py migrate
    python manage.py download-countries

    # Frontend Configuration
    cat <<EOF > "$ADVENTURELOG_DIR/frontend/.env"
PUBLIC_SERVER_URL=http://${LOCAL_IP}:8000
BODY_SIZE_LIMIT=Infinity
ORIGIN='http://${LOCAL_IP}:3000'
EOF

    # Frontend Setup
    cd "$ADVENTURELOG_DIR/frontend"
    pnpm install
    pnpm build

    echo "${RELEASE}" > "$VERSION_FILE"

    {
        echo ""
        echo "Django-Credentials"
        echo "Django Admin User: $DJANGO_ADMIN_USER"
        echo "Django Admin Password: $DJANGO_ADMIN_PASS"
    } >> "$CREDS_FILE"

    # Save Secrets
    {
        echo ""
        echo "AdventureLog-Credentials"
        echo "AdventureLog Database User: $DB_USER"
        echo "AdventureLog Database Password: $DB_PASS"
        echo "AdventureLog Database Name: $DB_NAME"
        echo "AdventureLog Secret: $SECRET_KEY"
    } >> "$CREDS_FILE"

    msg_ok "Installed AdventureLog"
}

# Function to set up Django Admin
setup_django_admin() {
    msg_info "Setting up Django Admin"

    cd "$ADVENTURELOG_DIR/backend/server"
    source venv/bin/activate
    python manage.py shell << EOF
from django.contrib.auth import get_user_model
UserModel = get_user_model()
user = UserModel.objects.create_user('$DJANGO_ADMIN_USER', password='$DJANGO_ADMIN_PASS')
user.is_superuser = True
user.is_staff = True
user.save()
EOF

    msg_ok "Setup Django Admin"
}

# Function to create and start services without systemd
create_services() {
    msg_info "Starting AdventureLog Backend and Frontend Services"

    # Backend Service
    cd "$ADVENTURELOG_DIR/backend/server"
    source venv/bin/activate
    nohup python manage.py runserver 0.0.0.0:8000 > /dev/null 2>&1 &

    # Frontend Service
    cd "$ADVENTURELOG_DIR/frontend"
    nohup pnpm start > /dev/null 2>&1 &

    msg_ok "Started AdventureLog Backend and Frontend Services"
    echo "Note: Services are running in the background using 'nohup'. To stop them, find their PIDs using 'ps aux | grep python' and 'ps aux | grep pnpm' and kill them manually."
}

# Function to clean up unnecessary files
cleanup() {
    msg_info "Cleaning up"
    sudo apt-get -y autoremove
    sudo apt-get -y autoclean
    msg_ok "Cleaned"
}

# ------------------------------- Main Script ---------------------------------

install_dependencies
setup_nodejs
setup_postgresql
setup_database
install_adventurelog
setup_django_admin
create_services
cleanup

# Display Credentials
echo -e "\n\e[34m[INFO]\e[0m Installation Complete. Credentials saved to $CREDS_FILE"
cat "$CREDS_FILE"

# Optional: Display message of the day or additional instructions
echo -e "\nTo access AdventureLog:"
echo "Backend: http://$(hostname -I | awk '{print $1}'):8000"
echo "Frontend: http://$(hostname -I | awk '{print $1}'):3000"
echo "Django Admin Username: djangoadmin"
echo "Django Admin Password: [Refer to $CREDS_FILE]"
