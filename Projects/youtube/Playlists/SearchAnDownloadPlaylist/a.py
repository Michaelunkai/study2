import os
from googleapiclient.discovery import build
import yt_dlp

# Set your API key here
API_KEY = 'AIzaSyDsDMEoP24LLQn3Df679YxcsO_jE0nqrWQ'

def search_playlists(query):
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    # Search for playlists based on the query
    request = youtube.search().list(
        part='snippet',
        maxResults=20,  # Number of playlists to retrieve
        q=query,  # Search query
        type='playlist'  # Limit search to playlists
    )
    response = request.execute()

    # Extract playlist information
    playlists = []
    for item in response['items']:
        playlists.append({
            'id': item['id']['playlistId'],
            'title': item['snippet']['title'],
            'channel': item['snippet']['channelTitle']
        })

    # Retrieve content details for each playlist to get video count
    for playlist in playlists:
        playlist_request = youtube.playlists().list(
            part='contentDetails',
            id=playlist['id']
        )
        playlist_response = playlist_request.execute()
        playlist['video_count'] = int(playlist_response['items'][0]['contentDetails']['itemCount'])

    # Sort playlists by the number of videos (descending order)
    playlists_sorted = sorted(playlists, key=lambda x: -x['video_count'])

    return playlists_sorted

def download_playlist_videos(playlist_url, download_path):
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])

def main():
    # Ask user for search query
    search_query = input("Enter your search query for YouTube playlists: ")

    # Get playlists based on the search query
    playlists = search_playlists(search_query)

    # Display the sorted playlists
    print(f"\nTop 20 YouTube Playlists related to '{search_query}':\n")
    for idx, playlist in enumerate(playlists, start=1):
        print(f"{idx}. {playlist['title']} by {playlist['channel']} - {playlist['video_count']} videos")

    # Ask user to select a playlist
    selected_index = int(input("\nSelect a playlist by number to download its videos: ")) - 1
    selected_playlist = playlists[selected_index]

    # Construct the playlist URL
    playlist_url = f"https://www.youtube.com/playlist?list={selected_playlist['id']}"

    # Set the download path
    download_path = r'C:\users\micha\downloads'

    # Ensure the download path exists
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Download videos from the selected playlist
    download_playlist_videos(playlist_url, download_path)

if __name__ == '__main__':
    main()
