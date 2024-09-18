# Variables
$InterfaceAlias = "Ethernet"
$IPAddress = "192.168.1.100"
$SubnetMask = "255.255.255.0"
$Gateway = "192.168.1.1"
$DNS1 = "8.8.8.8"
$DNS2 = "8.8.4.4"

# Configure IP Address
New-NetIPAddress `
    -InterfaceAlias $InterfaceAlias `
    -IPAddress $IPAddress `
    -PrefixLength 24 `
    -DefaultGateway $Gateway

# Configure DNS Servers
Set-DnsClientServerAddress `
    -InterfaceAlias $InterfaceAlias `
    -ServerAddresses ($DNS1, $DNS2)
