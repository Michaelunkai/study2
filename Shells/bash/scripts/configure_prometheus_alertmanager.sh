#!/bin/ 

# Configure Prometheus to use Alertmanager
sudo bash -c 'cat <<EOF > /etc/prometheus/prometheus.yml
alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - localhost:9093

rule_files:
  - "alert.rules.yml"
EOF'

# Create an alert rules file
sudo bash -c 'cat <<EOF > /etc/prometheus/alert.rules.yml
groups:
- name: example
  rules:
  - alert: InstanceDown
    expr: up == 0
    for: 5m
    labels:
      severity: page
    annotations:
      summary: "Instance {{ \$labels.instance }} down"
      description: "{{ \$labels.instance }} of job {{ \$labels.job }} has been down for more than 5 minutes."
EOF'

# Restart Prometheus to apply the changes
sudo systemctl restart prometheus

# Configure Alertmanager
sudo bash -c 'cat <<EOF > /etc/alertmanager/alertmanager.yml
global:
  smtp_smarthost: 'smtp.example.com:587'
  smtp_from: 'alertmanager@example.com'

route:
  receiver: 'email'

receivers:
  - name: 'email'
    email_configs:
    - to: 'your-email@example.com'
EOF'

# Restart Alertmanager to apply the changes
sudo systemctl restart alertmanager
sudo systemctl status alertmanager

# Open Prometheus and Alertmanager in Chrome
cmd.exe /c start chrome http://localhost:9090
cmd.exe /c start chrome http://localhost:9093
