import os
from googleapiclient.discovery import build

# Set your API key here
API_KEY = 'your_api_key_here'

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

def main():
    # Ask user for search query
    search_query = input("Enter your search query for YouTube playlists: ")

    # Get playlists based on the search query
    playlists = search_playlists(search_query)

    # Display the sorted playlists
    print(f"\nTop 20 YouTube Playlists related to '{search_query}':\n")
    for idx, playlist in enumerate(playlists, start=1):
        print(f"{idx}. {playlist['title']} by {playlist['channel']} - {playlist['video_count']} videos")

if __name__ == '__main__':
    main()
