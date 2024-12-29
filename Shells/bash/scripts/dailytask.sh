#!/bin/bash

# Paths
SCRIPT_PATH="/mnt/c/study/shells/bash/scripts/SubsDaily.sh"
SERVICE_PATH="/etc/systemd/system/daily_task.service"
TIMER_PATH="/etc/systemd/system/daily_task.timer"

# Step 1: Create the shell script
echo "Creating the shell script..."
sudo mkdir -p "$(dirname "$SCRIPT_PATH")"
sudo bash -c "cat > $SCRIPT_PATH" <<'EOF'
#!/bin/bash
cd /mnt/c/backup/windowsapps
sudo apt install python3.10-venv -y
sudo apt install python3-venv -y
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
cd /mnt/c/study/programming/python/apps/youtube/Playlists/substoplaylist
python3 h.py
exec bash
EOF

# Make the shell script executable
sudo chmod +x "$SCRIPT_PATH"
echo "Shell script created and made executable at $SCRIPT_PATH."

# Step 2: Create the systemd service file
echo "Creating the systemd service file..."
sudo bash -c "cat > $SERVICE_PATH" <<EOF
[Unit]
Description=Daily task for running Python script
After=network.target

[Service]
ExecStart=$SCRIPT_PATH
WorkingDirectory=$(dirname "$SCRIPT_PATH")
User=$USER
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

[Install]
WantedBy=multi-user.target
EOF
echo "Systemd service file created at $SERVICE_PATH."

# Step 3: Create the systemd timer file
echo "Creating the systemd timer file..."
sudo bash -c "cat > $TIMER_PATH" <<EOF
[Unit]
Description=Run daily task at 16:52

[Timer]
OnCalendar=16:52
Persistent=true

[Install]
WantedBy=timers.target
EOF
echo "Systemd timer file created at $TIMER_PATH."

# Step 4: Enable and start the timer
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

echo "Enabling and starting the timer..."
sudo systemctl enable daily_task.timer
sudo systemctl start daily_task.timer

# Step 5: Verify the setup
echo "Verifying the setup..."
echo "Setup complete. Your script is scheduled to run daily at 16:52."

