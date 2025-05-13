# Define the path for the custom Sandbox configuration file on the Desktop
$wsbPath = "$env:USERPROFILE\Desktop\SandboxWithFolders.wsb"

# Create the XML content for the configuration file.
# This configuration maps:
#   - F:\ to C:\SandboxFDrive inside the sandbox.
#   - C:\Backup to C:\Backup inside the sandbox.
#   - C:\Study to C:\Study inside the sandbox.
$xmlContent = @"
<Configuration>
    <MappedFolders>
        <MappedFolder>
            <HostFolder>F:\</HostFolder>
            <SandboxFolder>C:\SandboxFDrive</SandboxFolder>
            <ReadOnly>false</ReadOnly>
        </MappedFolder>
        <MappedFolder>
            <HostFolder>C:\Backup</HostFolder>
            <SandboxFolder>C:\Backup</SandboxFolder>
            <ReadOnly>false</ReadOnly>
        </MappedFolder>
        <MappedFolder>
            <HostFolder>C:\Study</HostFolder>
            <SandboxFolder>C:\Study</SandboxFolder>
            <ReadOnly>false</ReadOnly>
        </MappedFolder>
    </MappedFolders>
</Configuration>
"@

# Write the XML content to the .wsb file
try {
    $xmlContent | Out-File -FilePath $wsbPath -Encoding UTF8 -Force
    Write-Host "Configuration file created at: $wsbPath"
}
catch {
    Write-Error "Failed to create the configuration file. $_"
    exit 1
}

# Launch Windows Sandbox with the newly created configuration file
try {
    Write-Host "Launching Windows Sandbox..."
    Start-Process $wsbPath
}
catch {
    Write-Error "Failed to launch Windows Sandbox. $_"
}
