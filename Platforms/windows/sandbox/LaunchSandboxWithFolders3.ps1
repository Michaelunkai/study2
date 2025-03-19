# Define the content of the Sandbox configuration file
$wsbContent = @"
<Configuration>
  <MappedFolders>
    <MappedFolder>
      <HostFolder>C:\backup</HostFolder>
      <SandboxFolder>C:\backup</SandboxFolder>
      <ReadOnly>true</ReadOnly>
    </MappedFolder>
    <MappedFolder>
      <HostFolder>C:\study</HostFolder>
      <SandboxFolder>C:\study</SandboxFolder>
      <ReadOnly>true</ReadOnly>
    </MappedFolder>
    <MappedFolder>
      <HostFolder>C:\wsl2</HostFolder>
      <SandboxFolder>C:\wsl2</SandboxFolder>
      <ReadOnly>true</ReadOnly>
    </MappedFolder>
    <MappedFolder>
      <HostFolder>C:\games</HostFolder>
      <SandboxFolder>C:\games</SandboxFolder>
      <ReadOnly>true</ReadOnly>
    </MappedFolder>
  </MappedFolders>
</Configuration>
"@

# Save the configuration to a temporary .wsb file
$wsbPath = "$env:TEMP\SandboxConfig.wsb"
$wsbContent | Out-File -FilePath $wsbPath -Encoding UTF8

# Launch Windows Sandbox with the configuration file
Start-Process -FilePath "C:\Windows\System32\WindowsSandbox.exe" -ArgumentList $wsbPath

