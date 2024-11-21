import tkinter as tk
from tkinter import filedialog
from PIL import Image
import pytesseract

# Set up Tesseract executable path if necessary
# Modify this path based on your Tesseract installation directory
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        image_path_entry.delete(0, tk.END)
        image_path_entry.insert(0, file_path)

def generate_text():
    image_path = image_path_entry.get()
    if image_path:
        try:
            img = Image.open(image_path)
            extracted_text = pytesseract.image_to_string(img)
            similar_text = create_similar_text(extracted_text)
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, similar_text)
        except Exception as e:
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, f"Error: {e}")

def create_similar_text(text):
    # This function generates similar text.
    # Currently, it returns the same text as a placeholder.
    # You can implement your own logic to modify the text.
    return text

# Set up the main application window
root = tk.Tk()
root.title("Image Text Similarity Generator")

# Set up the widgets
image_path_label = tk.Label(root, text="Image Path:")
image_path_label.grid(row=0, column=0, padx=10, pady=10)

image_path_entry = tk.Entry(root, width=50)
image_path_entry.grid(row=0, column=1, padx=10, pady=10)

browse_button = tk.Button(root, text="Browse", command=select_image)
browse_button.grid(row=0, column=2, padx=10, pady=10)

generate_button = tk.Button(root, text="Generate Text", command=generate_text)
generate_button.grid(row=1, column=0, columnspan=3, pady=10)

result_text = tk.Text(root, width=80, height=20)
result_text.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

# Run the application
root.mainloop()
