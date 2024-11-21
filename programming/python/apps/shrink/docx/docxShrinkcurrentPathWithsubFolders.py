import os
from docx import Document
from PIL import Image
from io import BytesIO

def compress_images_in_docx(docx_path, quality=40):
    try:
        document = Document(docx_path)
    except Exception as e:
        print(f"Error opening {docx_path}: {e}")
        return

    for rel in document.part.rels.values():
        if "image" in rel.target_ref:
            img_part = rel.target_part
            image_stream = BytesIO(img_part.blob)
            try:
                image = Image.open(image_stream)
                compressed_stream = BytesIO()
                image.save(compressed_stream, format=image.format, optimize=True, quality=quality)
                img_part._blob = compressed_stream.getvalue()
            except Exception as e:
                print(f"Error processing image in {docx_path}: {e}")
                continue

    try:
        document.save(docx_path)
        print(f"Compressed and saved: {docx_path}")
    except Exception as e:
        print(f"Error saving {docx_path}: {e}")

def process_all_docx_files_in_directory(directory, quality=40, max_depth=12):
    for root, _, files in os.walk(directory):
        # Calculate the current depth
        depth = root[len(directory):].count(os.sep)
        if depth > max_depth:
            continue
        for filename in files:
            if filename.lower().endswith('.docx'):
                docx_path = os.path.join(root, filename)
                print(f"Processing {docx_path}...")
                compress_images_in_docx(docx_path, quality)

if __name__ == "__main__":
    current_directory = os.getcwd()
    process_all_docx_files_in_directory(current_directory)
