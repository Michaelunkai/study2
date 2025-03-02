# Script to fix Wi-Fi issues

# Release and renew IP configuration
ipconfig /release
ipconfig /renew

# Clear DNS client cache
Clear-DnsClientCache

# Restart Wi-Fi adapter
Restart-NetAdapter -InterfaceDescription "Wi-Fi"

# Show detailed wireless network information
netsh wlan show interfaces

# Reset Winsock Catalog
netsh winsock reset

# Reset firewall rules
netsh advfirewall reset

# Display network configuration information
Get-NetIPAddress

# Check Wi-Fi auto-configuration state
netsh wlan show settings

# View network event log
Get-EventLog -LogName System -Source Microsoft-Windows-WLAN-AutoConfig

# Check wireless network drivers
Get-NetAdapter | Where-Object { $_.InterfaceDescription -like '*Wireless*' } | Get-NetAdapterDriver

# Flush ARP cache
netsh interface ip delete arpcache

# Check Wi-Fi power management settings
powercfg /query SCHEME_CURRENT SUB_SLEEP STANDBYIDLE

# Reset network stack (TCP/IP, Winsock, ARP)
netsh int ip reset
netsh winsock reset
netsh interface ip delete arpcache

# Display network statistics
netstat -s

# Display routing table
route print

# Show active network connections
Get-NetTCPConnection

# Check network connectivity to a specific address (replace example.com with an actual address)
Test-NetConnection -ComputerName example.com -Port 80

# Display network interface configuration
Get-NetIPConfiguration

# Reset network adapter configuration
netsh interface ip reset

# Show DNS client settings
Get-DnsClientServerAddress

# Display network adapter configuration
Get-NetAdapterConfiguration
