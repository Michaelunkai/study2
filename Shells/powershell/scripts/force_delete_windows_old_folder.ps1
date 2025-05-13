# Grant full control to the current user for the windows.old folder and its contents
takeown /F "C:\Windows.old" /A /R /D Y
icacls "C:\Windows.old" /grant administrators:F /T

# Remove the windows.old folder
Remove-Item -Path "C:\Windows.old" -Recurse -Force
