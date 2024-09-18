from googleapiclient.discovery import build

# Define your API key
API_KEY = ""

def main():
    # Build the YouTube Data API service using your API key
    youtube = build("youtube", "v3", developerKey=API_KEY)

    # Replace "PLAYLIST_ID_HERE" with the playlist ID you want to retrieve videos from
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

    # Create a list to store video details
    videos_details = []

    # Iterate over each video in the playlist
    for playlist_item in playlist_items:
        video_title = playlist_item["snippet"]["title"]
        video_id = playlist_item["snippet"]["resourceId"]["videoId"]
        
        # Retrieve the duration of the video from its content details
        video_response = youtube.videos().list(
            part="contentDetails",
            id=video_id
        ).execute()
        video_duration = video_response["items"][0]["contentDetails"]["duration"]
        
        # Convert ISO 8601 duration to seconds
        duration_seconds = iso8601_duration_to_seconds(video_duration)
        
        # Append video details to the list
        videos_details.append({"title": video_title, "duration": duration_seconds})

    # Sort videos by duration
    sorted_videos = sorted(videos_details, key=lambda x: x["duration"])

    # Print the details of each video
    for video in sorted_videos:
        print(f"Video Title: {video['title']}")
        print(f"Video Duration: {format_duration(video['duration'])}\n")

def iso8601_duration_to_seconds(duration):
    # Convert ISO 8601 duration format to seconds
    parts = duration.split('T')
    duration = parts[-1]
    seconds = 0
    for part in duration.split('P')[-1].split('T'):
        if 'H' in part:
            seconds += int(part.split('H')[0]) * 3600
        elif 'M' in part:
            seconds += int(part.split('M')[0]) * 60
        elif 'S' in part:
            seconds += int(part.split('S')[0])
    return seconds

def format_duration(seconds):
    # Convert seconds to HH:MM:SS format
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

if __name__ == "__main__":
    main()

