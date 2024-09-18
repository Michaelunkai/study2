#!/bin/ 

cleanmgr /D C /F /SILENT;
del /q /f /s "$TEMP/*" /S /F;
del /q /f /s C:/Windows/Temp/*.* /S /F;
DiskCleanup /SAGERUN:1 /NUI;
dism.exe /online /cleanup-image /startcomponentcleanup /quiet;
vssadmin delete shadows /for=C: /oldest /quiet;
dism.exe /online /cleanup-image /analyzecomponentstore /quiet;
dism.exe /online /cleanup-image /startcomponentcleanup /resetbase /quiet;
powercfg.exe /hibernate off /quiet;
for eventlog in $(wevtutil.exe el); do wevtutil.exe cl "$eventlog" /quiet; done
;
dism.exe /online /cleanup-image /spsuperseded /quiet
