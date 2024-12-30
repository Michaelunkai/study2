#!/bin/bash

# Define variables
PLEX_WEBCLIENT_DIR=$(find /usr/lib/plexmediaserver/Resources/Plug-ins-* -type d -name "WebClient.bundle" | head -n 1)/Contents/Resources
USER_JS_URL="https://gist.githubusercontent.com/ZigZagT/b992bda82b5f7a2c9d214110273d3f3c/raw/Plex%2520Playback%2520Speed.user.js"
USER_JS_PATH="$PLEX_WEBCLIENT_DIR/js/PlexPlaybackSpeed.js"
INDEX_HTML="$PLEX_WEBCLIENT_DIR/index.html"
STARTUP_SCRIPT="/etc/plex_inject_playback_speed.sh"

# Check if Plex WebClient directory exists
if [ ! -d "$PLEX_WEBCLIENT_DIR" ]; then
    echo "Plex WebClient directory not found at $PLEX_WEBCLIENT_DIR"
    exit 1
fi

# Download the playback speed script
echo "Downloading Plex Playback Speed script..."
wget -O "$USER_JS_PATH" "$USER_JS_URL" || { echo "Download failed"; exit 1; }

# Modify index.html to include the script if not already included
if ! grep -q "PlexPlaybackSpeed.js" "$INDEX_HTML"; then
    echo "Injecting playback speed script into index.html..."
    sed -i 's#</head>#<script src="/web/js/PlexPlaybackSpeed.js"></script></head>#' "$INDEX_HTML"
else
    echo "Playback speed script already injected."
fi

# Create a startup script to re-inject on Plex restart (handles updates)
echo "Creating startup script for automatic injection..."
cat <<EOF > "$STARTUP_SCRIPT"
#!/bin/bash
# Wait for Plex to start
sleep 10
# Re-download the playback speed script
wget -O "$USER_JS_PATH" "$USER_JS_URL"
# Ensure index.html includes the script
grep -q "PlexPlaybackSpeed.js" "$INDEX_HTML" || sed -i 's#</head>#<script src="/web/js/PlexPlaybackSpeed.js"></script></head>#' "$INDEX_HTML"
EOF

chmod +x "$STARTUP_SCRIPT"

# Ensure the startup script runs on Plex restart
# This example uses systemd. Adjust if you're using a different init system.

SERVICE_FILE="/etc/systemd/system/plex_playback_speed.service"

if [ ! -f "$SERVICE_FILE" ]; then
    echo "Creating systemd service for playback speed injection..."
    cat <<EOF > "$SERVICE_FILE"
[Unit]
Description=Plex Playback Speed Injection
After=plexmediaserver.service
Requires=plexmediaserver.service

[Service]
Type=oneshot
ExecStart=/bin/bash $STARTUP_SCRIPT
RemainAfterExit=true

[Install]
WantedBy=plexmediaserver.service
EOF

    # Reload systemd and enable the service
    systemctl daemon-reload
    systemctl enable plex_playback_speed.service
    systemctl start plex_playback_speed.service
else
    echo "Systemd service for playback speed injection already exists."
fi

echo "Playback speed injection setup completed."

sudo systemctl restart plexmediaserver
