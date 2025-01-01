# Set your Proxmox server details
$ProxmoxServer = "172.30.244.9"
$Username = "admin"
$Password = "password"

# Set the VM ID (replace with your VM ID)
$VMID = "100"

# Create a base64-encoded credential for authentication
$Base64AuthInfo = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("${Username}:${Password}")))

# Define the Proxmox API endpoint for starting a VM
$ProxmoxAPIEndpoint = "https://${ProxmoxServer}/api2/json/nodes/${ProxmoxServer}/qemu/${VMID}/status/start"

# Send the HTTP request to start the VM
Invoke-RestMethod -Uri $ProxmoxAPIEndpoint -Method Post -Headers @{Authorization=("Basic {0}" -f $Base64AuthInfo)}
