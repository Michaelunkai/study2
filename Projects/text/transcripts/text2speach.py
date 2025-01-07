from gtts import gTTS
import pygame
import os
import tempfile

def text_to_speech(text, language='en'):
    # Create a gTTS object
    tts = gTTS(text=text, lang=language, slow=False)

    # Create a temporary file to save the audio
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp_filename = temp_file.name

    # Save the audio file
    tts.save(temp_filename)

    # Initialize pygame mixer
    pygame.mixer.init()

    # Load the audio file
    pygame.mixer.music.load(temp_filename)

    # Play the audio file
    pygame.mixer.music.play()

    # Wait for the playback to finish
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Clean up the temporary file
    temp_file.close()
    os.remove(temp_filename)

if __name__ == "__main__":
    # Get input text from the user in the terminal
    text = input("Enter the text you want to convert to speech: ")

    # Call the function to convert text to speech
    text_to_speech(text)