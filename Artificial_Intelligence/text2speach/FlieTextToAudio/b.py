import os
import pyttsx3
from PyPDF2 import PdfFileReader
import docx

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def read_pdf_file(file_path):
    pdf = PdfFileReader(open(file_path, 'rb'))
    text = ""
    for page in range(pdf.getNumPages()):
        text += pdf.getPage(page).extract_text()
    return text

def read_word_file(file_path):
    doc = docx.Document(file_path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])

def read_file(file_path):
    _, ext = os.path.splitext(file_path)
    if ext in ['.txt', '.py', '.js', '.html', '.css']:
        return read_text_file(file_path)
    elif ext == '.pdf':
        return read_pdf_file(file_path)
    elif ext == '.docx':
        return read_word_file(file_path)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")

def text_to_speech(text, output_path):
    engine = pyttsx3.init()
    
    # Set properties for more human-like voice
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 50)  # Decrease rate for more natural speech
    volume = engine.getProperty('volume')
    engine.setProperty('volume', 1.0)  # Max volume
    
    # Set voice (using a more natural-sounding voice if available)
    voices = engine.getProperty('voices')
    for voice in voices:
        if "Zira" in voice.name or "David" in voice.name:  # Example voices for SAPI5 on Windows
            engine.setProperty('voice', voice.id)
            break
    
    engine.save_to_file(text, output_path)
    engine.runAndWait()

def main():
    file_path = input("Enter the full path to the file: ")
    
    try:
        content = read_file(file_path)
        output_path = os.path.splitext(file_path)[0] + '.mp3'
        
        print(f"Converting text to speech and saving as {output_path}...")
        text_to_speech(content, output_path)
        
        print(f"Audio file created successfully at {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
