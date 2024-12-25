import os
from dotenv import load_dotenv
import streamlit as st
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_community.chat_models import ChatOpenAI
from gtts import gTTS
from io import BytesIO
import base64

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("Please set your OpenAI API key in the .env file.")

# Streamlit app
st.title("YouTube Video Summarizer and Tutorial Generator with Audio Playback")
video_url = st.text_input("Enter YouTube video URL:")

def text_to_audio(text):
    """Convert text to audio and return the audio file."""
    tts = gTTS(text)
    audio_file = BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)
    audio_base64 = base64.b64encode(audio_file.read()).decode()
    return f"data:audio/mp3;base64,{audio_base64}"

if video_url:
    try:
        # Extract video ID from URL
        video_id = YouTube(video_url).video_id

        # Fetch transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([entry['text'] for entry in transcript])

        # Initialize OpenAI model
        chat = ChatOpenAI(model="gpt-3.5-turbo", api_key=openai_api_key)

        # Generate a detailed summary (minimum 300 words)
        st.write("Generating a detailed summary...")
        summary_prompt = f"""
        The following text is a transcript of a YouTube video. Summarize it in at least 300 words:
        
        {transcript_text}
        """
        summary = chat.predict(summary_prompt)

        # Generate step-by-step tutorial
        st.write("Generating a step-by-step tutorial...")
        tutorial_prompt = f"""
        The following text is a transcript of a YouTube video. Create a step-by-step tutorial based on the content of the video. Ensure the tutorial is clear and easy to follow:
        
        {transcript_text}
        """
        tutorial = chat.predict(tutorial_prompt)

        # Display results
        st.subheader("Detailed Summary (300+ words):")
        st.write(summary)
        audio_summary = text_to_audio(summary)
        st.audio(audio_summary, format="audio/mp3", start_time=0)

        st.subheader("Step-by-Step Tutorial:")
        st.write(tutorial)
        audio_tutorial = text_to_audio(tutorial)
        st.audio(audio_tutorial, format="audio/mp3", start_time=0)

    except Exception as e:
        st.error(f"An error occurred: {e}")
