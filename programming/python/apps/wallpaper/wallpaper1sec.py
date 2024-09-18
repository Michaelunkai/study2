import ctypes
import os
import time

def change_wallpaper(image_path):
    SPI_SET_WALLPAPER = 20
    SPIF_UPDATEINIFILE = 0x01
    SPIF_SENDCHANGE = 0x02

    # Change wallpaper
    ctypes.windll.user32.SystemParametersInfoW(SPI_SET_WALLPAPER, 0, image_path, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)

def get_image_files(directory):
    image_files = []
    for file in os.listdir(directory):
        if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
            image_files.append(os.path.join(directory, file))
    return image_files

if __name__ == "__main__":
    wallpaper_directory = r"C:/Users/micha/pictures/back/"
    image_files = get_image_files(wallpaper_directory)
    if not image_files:
        print("No image files found in the specified directory.")
    else:
        while True:
            for image_file in image_files:
                change_wallpaper(image_file)
                time.sleep(1)  # Change wallpaper every 1 seconds
