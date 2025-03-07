import os
import yt_dlp

# Define paths
SONGS_FILE = "C:\Users\micha\Downloads\songs.txt"
DOWNLOAD_FOLDER = r"C:\Users\micha\Downloads\music"

# Ensure the download folder exists
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def read_song_list(filename):
    """Read songs from the provided text file."""
    if not os.path.exists(filename):
        print(f"Error: {filename} not found!")
        return []
    
    with open(filename, "r", encoding="utf-8") as f:
        songs = [line.strip().split(": ", 1)[-1] for line in f if line.strip()]
    
    return songs

def sanitize_filename(name):
    """Sanitize filenames to remove problematic characters."""
    return "".join(c for c in name if c.isalnum() or c in (" ", "-", "_")).rstrip()

def download_song(song_name):
    """Search and download the best audio match for a song from YouTube."""
    sanitized_name = sanitize_filename(song_name)
    output_path = os.path.join(DOWNLOAD_FOLDER, f"{sanitized_name}.mp3")
    
    if os.path.exists(output_path):
        print(f"Skipping '{song_name}' (Already Downloaded)")
        return
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
        'noplaylist': True,
        'default_search': 'ytsearch1',
    }

    print(f"Downloading: {song_name}...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([song_name])
        print(f"Downloaded: {song_name}\n")
    except Exception as e:
        print(f"Failed to download '{song_name}': {e}")

def main():
    """Main function to read songs and download them."""
    songs = read_song_list(SONGS_FILE)
    if not songs:
        print("No songs found in the list!")
        return
    
    print(f"Found {len(songs)} songs. Starting downloads...\n")
    
    for song in songs:
        download_song(song)

    print("✅ All downloads complete!")

if __name__ == "__main__":
    main()
