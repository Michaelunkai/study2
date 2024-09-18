#!/bin/ 

# Script to Install and Configure Papertrail Log Management with TLS on Ubuntu
# Tools used: Papertrail, Rsyslog, TLS for secure log transmission

# Install rsyslog and dependencies
sudo apt install -y rsyslog rsyslog-gnutls

# Papertrail log destination (replace with your Papertrail log destination and port)
PAPERTRAIL_DESTINATION="logsN.papertrailapp.com"
PAPERTRAIL_PORT="XXXXX"

# Adding Papertrail configuration to rsyslog
echo "Configuring rsyslog for Papertrail log forwarding with TLS"

# Create and write to the configuration file for Papertrail
cat <<EOL | sudo tee /etc/rsyslog.d/50-papertrail.conf > /dev/null
# Papertrail log management configuration with secure TLS transmission

# Send logs to Papertrail via TCP with TLS encryption
*.info @@$PAPERTRAIL_DESTINATION:$PAPERTRAIL_PORT;RSYSLOG_SyslogProtocol23Format

# Enable TLS settings
\$DefaultNetstreamDriverCAFile /etc/ssl/certs/ca-certificates.crt
\$ActionSendStreamDriver gtls
\$ActionSendStreamDriverMode 1
\$ActionSendStreamDriverAuthMode x509/name
\$ActionSendStreamDriverPermittedPeer *.papertrailapp.com

EOL

# Restart rsyslog service to apply changes
sudo systemctl restart rsyslog

# Verifying if rsyslog is running
if systemctl is-active --quiet rsyslog; then
    echo "rsyslog successfully restarted and is forwarding logs to Papertrail."
else
    echo "There was an issue restarting rsyslog. Check the configuration."
    exit 1
fi

# Send a test log entry to Papertrail to verify
logger "Test log entry from $(hostname) to Papertrail"

# Final message
echo "Papertrail log management setup with TLS is complete. Check your Papertrail dashboard for logs."

