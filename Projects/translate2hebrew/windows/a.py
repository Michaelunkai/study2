import os
from mtranslate import translate
from PyPDF2 import PdfFileReader

DOWNLOADS_PATH = r'C:\Users\micha\downloads'
CHUNK_SIZE = 5000  # Adjust the chunk size as needed

def translate_text(text, target_language='he'):
    try:
        translated_text = ""
        chunks = [text[i:i+CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE)]
        for chunk in chunks:
            translated_text += translate(chunk, target_language) + " "
        return translated_text.strip()
    except Exception as e:
        print(f"Error during translation: {e}")
        return ""

def translate_text_file(file_path, output_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        translated_text = translate_text(text)
        if translated_text:
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(translated_text)
            print(f"Translated text file saved as {output_path}")
        else:
            print("Translation failed.")
    except Exception as e:
        print(f"Error processing text file: {e}")

def extract_text_from_pdf(pdf_path):
    try:
        pdf_reader = PdfFileReader(pdf_path)
        text = ""
        for page_num in range(pdf_reader.getNumPages()):
            text += pdf_reader.getPage(page_num).extract_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def translate_pdf(file_path, output_path):
    try:
        text = extract_text_from_pdf(file_path)
        if text:
            translated_text = translate_text(text)
            if translated_text:
                with open(output_path, 'w', encoding='utf-8') as file:
                    file.write(translated_text)
                print(f"Translated PDF file saved as {output_path}")
            else:
                print("Translation failed.")
        else:
            print("Failed to extract text from PDF.")
    except Exception as e:
        print(f"Error processing PDF file: {e}")

def main():
    input_file_name = input("Enter the name of the text file or PDF file to translate (without path): ")
    input_file_path = os.path.join(DOWNLOADS_PATH, input_file_name)
    output_file_name = f"translated_{input_file_name}"
    output_file_path = os.path.join(DOWNLOADS_PATH, output_file_name)

    if input_file_name.lower().endswith('.txt'):
        translate_text_file(input_file_path, output_file_path)
    elif input_file_name.lower().endswith('.pdf'):
        translate_pdf(input_file_path, output_file_path)
    else:
        print("Unsupported file format. Please provide a .txt or .pdf file.")

if __name__ == "__main__":
    main()
