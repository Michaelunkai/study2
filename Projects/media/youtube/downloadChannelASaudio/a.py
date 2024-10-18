import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

try:
    import yt_dlp
except ImportError:
    print("yt-dlp is not installed. Please run 'pip install yt-dlp' and try again.")
    exit(1)

API_KEY = 'AIzaSyDsDMEoP24LLQn3Df679YxcsO_jE0nqrWQ'
DOWNLOAD_PATH = r"c:\Users\micha\Downloads\YouTube_Audio"
MAX_RETRIES = 3
RETRY_DELAY = 5

def sanitize_filename(title):
    return re.sub(r'[<>:"/\\|?*]', '', title)

def download_audio(video_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(DOWNLOAD_PATH, '%(title)s.%(ext)s'),
        'ignoreerrors': True,
    }

    for attempt in range(MAX_RETRIES):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            print(f"Download complete: {video_url}")
            return
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {video_url}: {str(e)}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
            else:
                print(f"Failed to download {video_url} after {MAX_RETRIES} attempts")

def get_channel_id(youtube, channel_url):
    if '/channel/' in channel_url:
        return channel_url.split('/channel/')[1]
    elif '/user/' in channel_url:
        username = channel_url.split('/user/')[1]
    elif '/@' in channel_url:
        username = channel_url.split('/@')[1]
    else:
        username = channel_url.split('/')[-1]

    try:
        response = youtube.search().list(
            part="id",
            q=username,
            type="channel",
            maxResults=1
        ).execute()
        if 'items' in response and response['items']:
            return response['items'][0]['id']['channelId']
    except HttpError as e:
        print(f"Error fetching channel: {str(e)}")

    raise ValueError("Unable to find channel ID")

def get_uploads_playlist_id(youtube, channel_id):
    try:
        response = youtube.channels().list(
            part="contentDetails",
            id=channel_id
        ).execute()
        
        if 'items' in response and response['items']:
            return response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    except HttpError as e:
        print(f"Error fetching uploads playlist ID: {str(e)}")

    raise ValueError("Unable to find uploads playlist ID")

def get_video_urls_from_playlist(youtube, playlist_id):
    video_urls = []
    next_page_token = None

    while True:
        try:
            response = youtube.playlistItems().list(
                part="snippet",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            for item in response['items']:
                video_urls.append(f"https://www.youtube.com/watch?v={item['snippet']['resourceId']['videoId']}")

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
        except HttpError as e:
            print(f"Error fetching videos from playlist: {str(e)}")
            break
    
    return video_urls

def download_channel_as_audio(channel_url):
    if not os.path.exists(DOWNLOAD_PATH):
        os.makedirs(DOWNLOAD_PATH)

    youtube = build('youtube', 'v3', developerKey=API_KEY)

    try:
        channel_id = get_channel_id(youtube, channel_url)
        print(f"Channel ID: {channel_id}")
        uploads_playlist_id = get_uploads_playlist_id(youtube, channel_id)
        print(f"Uploads playlist ID: {uploads_playlist_id}")
        video_urls = get_video_urls_from_playlist(youtube, uploads_playlist_id)
        print(f"Found {len(video_urls)} videos. Downloading...")

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(download_audio, video_url) for video_url in video_urls]
            for future in as_completed(futures):
                future.result()

        print("All available videos have been processed.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    channel_url = input("Enter YouTube channel URL: ")
    download_channel_as_audio(channel_url)

if __name__ == "__main__":
    main()
