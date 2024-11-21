import os
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

# Function to save transcript to a file
def save_transcript_to_file(video_id, transcript):
    file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), f"{video_id}.txt")
    with open(file_path, "w") as file:
        for sentence in transcript:
            file.write(sentence['text'] + "\n")

# Example usage
if __name__ == "__main__":
    youtube_url = input("Enter the YouTube URL: ")
    video_id = extract_video_id(youtube_url)

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        if transcript:
            print_transcript(transcript)
            save_transcript_to_file(video_id, transcript)
            print(f"Transcript saved to {video_id}.txt")
        else:
            print("Transcript not available for this video.")
    except Exception as e:
        print("An error occurred:", e)