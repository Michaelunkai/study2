#!/bin/ 

Get-AppxPackage -allusers Microsoft.WindowsStore | foreach {Add-AppxPackage -register "$($_.InstallLocation)\appxmanifest.xml" -DisableDevelopmentMode}
