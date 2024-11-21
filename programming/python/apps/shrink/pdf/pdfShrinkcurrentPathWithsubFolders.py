import os
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
from io import BytesIO

def compress_images_in_pdf(pdf_path, quality=40):
    try:
        reader = PdfReader(pdf_path)
        writer = PdfWriter()

        for page in reader.pages:
            # Iterate over images within the page (simplified version)
            if '/XObject' in page['/Resources']:
                xObject = page['/Resources']['/XObject'].get_object()
                for obj in xObject:
                    if xObject[obj]['/Subtype'] == '/Image':
                        image_bytes = xObject[obj].get_data()
                        try:
                            image = Image.open(BytesIO(image_bytes))
                            compressed_stream = BytesIO()
                            image.save(compressed_stream, format=image.format, optimize=True, quality=quality)
                            xObject[obj]._data = compressed_stream.getvalue()
                        except Exception as e:
                            print(f"Error processing image in {pdf_path}: {e}")
                            continue

            writer.add_page(page)

        output_path = pdf_path
        with open(output_path, 'wb') as f:
            writer.write(f)
        print(f"Compressed and saved: {pdf_path}")
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")

def process_all_pdf_files_in_directory(directory, quality=40, max_depth=12):
    for root, _, files in os.walk(directory):
        # Calculate the current depth
        depth = root[len(directory):].count(os.sep)
        if depth > max_depth:
            continue
        for filename in files:
            if filename.lower().endswith('.pdf'):
                pdf_path = os.path.join(root, filename)
                print(f"Processing {pdf_path}...")
                compress_images_in_pdf(pdf_path, quality)

if __name__ == "__main__":
    current_directory = os.getcwd()
    process_all_pdf_files_in_directory(current_directory)
