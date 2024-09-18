import os
import subprocess
from tqdm import tqdm
import humanize
import shutil
import zipfile
import requests
import sys
import concurrent.futures

FFMPEG_URL = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
FFMPEG_ZIP = "ffmpeg.zip"
FFMPEG_DIR = "ffmpeg"

def download_file(url, filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total_size = int(r.headers.get('content-length', 0))
        with open(filename, 'wb') as f, tqdm(
            desc=filename,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as progress_bar:
            for data in r.iter_content(chunk_size=1024):
                size = f.write(data)
                progress_bar.update(size)

def setup_ffmpeg():
    if not os.path.exists(FFMPEG_DIR):
        print("Downloading FFmpeg...")
        download_file(FFMPEG_URL, FFMPEG_ZIP)

        print("Extracting FFmpeg...")
        with zipfile.ZipFile(FFMPEG_ZIP, 'r') as zip_ref:
            zip_ref.extractall(FFMPEG_DIR)

        os.remove(FFMPEG_ZIP)

    ffmpeg_path = os.path.join(os.getcwd(), FFMPEG_DIR, "ffmpeg-master-latest-win64-gpl", "bin")
    os.environ["PATH"] += os.pathsep + ffmpeg_path
    print(f"FFmpeg set up in: {ffmpeg_path}")

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False

def get_file_size(file_path):
    return os.path.getsize(file_path)

def shrink_file(input_file, output_file):
    if input_file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        cmd = [
            "ffmpeg", "-i", input_file,
            "-c:v", "libx264", "-preset", "fast", "-crf", "28",
            "-c:a", "aac", "-b:a", "128k",
            "-y", output_file
        ]
    elif input_file.lower().endswith(('.mp3', '.wav', '.flac', '.aac')):
        cmd = [
            "ffmpeg", "-i", input_file,
            "-c:a", "aac", "-b:a", "128k",
            "-y", output_file
        ]
    else:
        print(f"Unsupported file format: {input_file}")
        return False

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error processing {input_file}: {e}")
        return False

def process_file(file, path, results):
    input_file = os.path.join(path, file)
    output_file = os.path.join(path, f"shrunk_{file}")

    original_size = get_file_size(input_file)

    if shrink_file(input_file, output_file):
        new_size = get_file_size(output_file)

        if new_size < original_size:
            os.remove(input_file)
            os.rename(output_file, input_file)
            results.append((file, original_size, new_size))
        else:
            os.remove(output_file)
            print(f"Couldn't reduce size of {file}. Keeping original.")
    else:
        print(f"Failed to process {file}. Skipping.")

def main():
    if not check_ffmpeg():
        print("FFmpeg not found. Setting up FFmpeg...")
        setup_ffmpeg()
        if not check_ffmpeg():
            print("Failed to set up FFmpeg. Please install it manually.")
            return

    path = input("Enter the directory path containing video/audio files: ").strip()

    if not os.path.isdir(path):
        print("Invalid directory path.")
        return

    supported_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.mp3', '.wav', '.flac', '.aac')
    files = [f for f in os.listdir(path) if f.lower().endswith(supported_extensions)]

    if not files:
        print("No supported video or audio files found in the directory.")
        return

    print(f"Found {len(files)} supported files. Processing...")

    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = [executor.submit(process_file, file, path, results) for file in files]
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Processing files"):
            pass

    print("\nProcessing complete. Results:")
    for file, original, new in results:
        print(f"{file}:")
        print(f"  Original size: {humanize.naturalsize(original)}")
        print(f"  New size: {humanize.naturalsize(new)}")
        print(f"  Reduction: {(1 - new/original)*100:.2f}%")
        print()

if __name__ == "__main__":
    main()
