#!/bin/ 

sfc /scannow;
repair-WindowsImage -ScanHealth;
Repair-WindowsImage -Online -CheckHealth;
Repair-Volume -DriveLetter C -Scan;
DISM /Online /Cleanup-Image /RestoreHealth;
chkdsk /f /r;
wmic product get name;
dism.exe /online /cleanup-image /startcomponentcleanup;
sfc /verifyonly;
reg.exe add HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Windows.old /t REG_DWORD /d 0 /f;
gpupdate /force;
netsh winsock reset;
netsh int ip reset;
netsh advfirewall reset;
netsh branchcache reset;
netsh winhttp reset proxy;
net stop wuauserv;
net stop cryptSvc;
net stop bits;
net stop msiserver;
ren C:\Windows\SoftwareDistribution SoftwareDistribution.old;
ren C:\Windows\System32\catroot2 catroot2.old;
