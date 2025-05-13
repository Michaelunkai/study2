import yt_dlp
import os

def download_audio(url, output_path):
    # Configure yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        # Options for faster download
        'concurrent_fragment_downloads': 3,
        'throttledratelimit': 100000,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("Starting download...")
            ydl.download([url])
            print(f"\nDownload completed! File saved to: {output_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Set the output path
    output_path = r"C:\users\micha\videos\audiobooks"
    
    # Create the directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    
    while True:
        url = input("Enter YouTube URL (or 'q' to quit): ")
        if url.lower() == 'q':
            break
            
        download_audio(url, output_path)
        print("\nReady for next URL...")
