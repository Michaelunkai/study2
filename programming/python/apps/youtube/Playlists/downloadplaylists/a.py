from pytube import Playlist, YouTube

def download_playlist(url):
    playlist = Playlist(url)
    
    for video_url in playlist.video_urls:
        try:
            yt = YouTube(video_url)
            print("Downloading:", yt.title)
            yt.streams.get_highest_resolution().download()  # Downloads the highest resolution stream
            print("Download completed.")
        except Exception as e:
            print("Error downloading", video_url, ":", e)

if __name__ == "__main__":
    print("Please enter the URL of the YouTube playlist:")
    playlist_url = input()
    download_playlist(playlist_url)
