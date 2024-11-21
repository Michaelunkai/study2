from youtube_transcript_api import YouTubeTranscriptApi

# Function to extract video ID from YouTube URL
def extract_video_id(url):
    video_id = url.split('?v=')[-1]
    return video_id

# Function to print transcript with better formatting
def print_transcript(transcript):
    print("Transcript:")
    print("-" * 40)  # Print a separator line
    for sentence in transcript:
        print(f"{sentence['text']}\n")  # Print each sentence with a newline
    print("-" * 40)  # Print a separator line

# Example usage
if __name__ == "__main__":
    youtube_url = input("Enter the YouTube URL: ")
    video_id = extract_video_id(youtube_url)
    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        if transcript:
            print_transcript(transcript)
        else:
            print("Transcript not available for this video.")
    except Exception as e:
        print("An error occurred:", e)
