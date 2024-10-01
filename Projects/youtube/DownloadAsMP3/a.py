from pytube import YouTube
from moviepy.editor import *
import os
import re

def download_youtube_as_mp3():
    # Ask for the YouTube URL
    url = input("Enter YouTube URL: ")

    # Specify the download path
    download_path = "C:/Users/micha/Downloads"

    try:
        # Create a YouTube object
        yt = YouTube(url)

        # Get the highest quality audio stream
        audio_stream = yt.streams.filter(only_audio=True).first()

        # Sanitize the title to create a valid filename
        safe_title = re.sub(r'[<>:"/\\|?*]', '', yt.title)
        temp_audio_file = os.path.join(download_path, "temp_audio.mp4")
        final_audio_mp3 = os.path.join(download_path, f"{safe_title}.mp3")

        # Download the audio stream
        print(f"Downloading audio from {yt.title}...")
        audio_stream.download(output_path=download_path, filename="temp_audio.mp4")

        # Convert the downloaded file to mp3 using moviepy
        print("Converting to mp3 format...")
        audio_clip = AudioFileClip(temp_audio_file)
        audio_clip.write_audiofile(final_audio_mp3)
        audio_clip.close()

        # Remove the temporary audio file
        os.remove(temp_audio_file)

        print(f"Download and conversion complete: {final_audio_mp3}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    download_youtube_as_mp3()
