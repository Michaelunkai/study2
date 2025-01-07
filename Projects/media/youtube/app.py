import os
import subprocess

# Function to download and convert videos to MP3
def download_channel_videos(channel_url):
    # Define the download directory
    download_dir = '/mnt/c/Users/micha/Downloads'
    os.makedirs(download_dir, exist_ok=True)
    os.chdir(download_dir)

    # Download all videos from the channel
    command = [
        'yt-dlp',
        '--extract-audio',
        '--audio-format', 'mp3',
        '--yes-playlist',
        channel_url
    ]

    subprocess.run(command)

if __name__ == "__main__":
    channel_url = input("Enter the YouTube channel URL: ")
    download_channel_videos(channel_url)
