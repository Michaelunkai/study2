from googleapiclient.discovery import build

# Define your API key
API_KEY = ""

def main():
    # Build the YouTube Data API service using your API key
    youtube = build("youtube", "v3", developerKey=API_KEY)

    # Replace "" with your playlist ID
    playlist_id = ""

    # Retrieve all videos in the specified playlist
    playlist_items_response = youtube.playlistItems().list(
        part="snippet,contentDetails",  # Add contentDetails to retrieve video duration
        playlistId=playlist_id,
        maxResults=50
    ).execute()

    playlist_items = playlist_items_response.get("items", [])

    if not playlist_items:
        print("No videos found in the playlist.")
        return

    # Print the details of each video
    for playlist_item in playlist_items:
        video_title = playlist_item["snippet"]["title"]
        video_id = playlist_item["snippet"]["resourceId"]["videoId"]
        
        # Retrieve the duration of the video from its content details
        video_response = youtube.videos().list(
            part="contentDetails",
            id=video_id
        ).execute()
        video_duration = video_response["items"][0]["contentDetails"]["duration"]
        
        print(f"Video Title: {video_title}")
        print(f"Video ID: {video_id}")
        print(f"Video Duration: {video_duration}\n")

if __name__ == "__main__":
    main()
