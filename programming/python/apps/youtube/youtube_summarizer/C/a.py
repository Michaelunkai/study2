import os
from dotenv import load_dotenv
import streamlit as st
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_community.chat_models import ChatOpenAI
from gtts import gTTS
from io import BytesIO
import base64
import re

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
   raise ValueError("Please set your OpenAI API key in the .env file.")

def extract_video_id(url):
   patterns = [
       r'(?:v=|/)([-\w]{11})',
       r'youtu\.be/([-\w]{11})',
       r'youtube\.com/embed/([-\w]{11})',
       r'youtube\.com/shorts/([-\w]{11})'
   ]
   for pattern in patterns:
       match = re.search(pattern, url)
       if match:
           return match.group(1)
   return None

def text_to_audio(text):
   tts = gTTS(text)
   audio_file = BytesIO()
   tts.write_to_fp(audio_file)
   audio_file.seek(0)
   audio_base64 = base64.b64encode(audio_file.read()).decode()
   return f"data:audio/mp3;base64,{audio_base64}"

def generate_code_tutorial(transcript_text):
   chat = ChatOpenAI(model="gpt-3.5-turbo", api_key=openai_api_key)
   
   code_prompt = f"""
   Based on the following video transcript, create a comprehensive tutorial that:
   1. Lists ALL commands and code snippets shown in the video in exact order
   2. Includes step-by-step instructions for each command
   3. Explains what each command/script does
   4. Includes any setup requirements or prerequisites
   5. Formats code blocks properly with appropriate syntax highlighting
   
   Transcript:
   {transcript_text}
   
   Format as a structured tutorial with clear sections and code blocks.
   """
   return chat.predict(code_prompt)

st.title("YouTube Video Code Tutorial Generator with Audio")
video_url = st.text_input("Enter YouTube video URL:")

if video_url:
   try:
       video_id = extract_video_id(video_url)
       if not video_id:
           st.error("Invalid YouTube URL. Please check the URL and try again.")
           st.stop()

       transcript = YouTubeTranscriptApi.get_transcript(video_id)
       transcript_text = " ".join([entry['text'] for entry in transcript])

       st.write("Generating code tutorial...")
       tutorial = generate_code_tutorial(transcript_text)

       st.subheader("Step-by-Step Code Tutorial:")
       st.markdown(tutorial)
       
       audio_tutorial = text_to_audio(tutorial)
       st.audio(audio_tutorial, format="audio/mp3", start_time=0)

   except Exception as e:
       st.error(f"An error occurred: {str(e)}")
