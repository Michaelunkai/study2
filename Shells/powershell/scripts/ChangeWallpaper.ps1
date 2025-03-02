# Set the path to the folder containing the images
$folderPath = "C:\Users\micha\Pictures\background"

# Get all jpg image files from the folder
$imageFiles = Get-ChildItem -Path $folderPath -Filter *.jpg -File

if ($imageFiles.Count -eq 0) {
    Write-Host "No JPG images found in the folder $folderPath"
    exit
}

# Add-Type definition for setting the wallpaper
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Wallpaper {
    [DllImport("user32.dll", CharSet = CharSet.Auto)]
    public static extern int SystemParametersInfo(int uAction, int uParam, string lpvParam, int fuWinIni);
    public const int SPI_SETDESKWALLPAPER = 20;
    public const int SPIF_UPDATEINIFILE = 0x01;
    public const int SPIF_SENDCHANGE = 0x02;
    public static void SetWallpaper(string path) {
        SystemParametersInfo(SPI_SETDESKWALLPAPER, 0, path, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE);
    }
}
"@

# Loop indefinitely to change the background every 5 seconds
while ($true) {
    foreach ($image in $imageFiles) {
        Write-Host "Setting wallpaper to $($image.FullName)"
        
        # Set the wallpaper
        [Wallpaper]::SetWallpaper($image.FullName)
        
        # Wait for 5 seconds before changing to the next image
        Start-Sleep -Seconds 5
    }
}
