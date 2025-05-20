# 1. Stop any NVIDIA-related processes ▸ 2. Fully reinstall the NVIDIA “app” (or GeForce Experience if the
#    App package isn’t yet in WinGet) ▸ 3. Launch NVCleanstall for an unattended clean-driver install
Stop-Process -Name "nv*" -Force -ErrorAction SilentlyContinue; `
& winget.exe uninstall --exact --id Nvidia.GeForceExperience  --silent 2>$null; `
& winget.exe install   --exact --id Nvidia.GeForceExperience  --silent `
                       --accept-package-agreements --accept-source-agreements; `
& "F:\backup\windowsapps\installed\NVCleanstall\NVCleanstall.exe" /auto /clean /silent /noreboot
