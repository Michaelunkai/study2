import tkinter as tk
from tkinter import filedialog
import os

def highlight_differences(text1, text2):
    highlighted_indices = []

    # Split the texts into lines
    lines1 = text1.split('\n')
    lines2 = text2.split('\n')

    # Compare each character in text2 with the corresponding character in text1
    for i, line2 in enumerate(lines2):
        for j, char2 in enumerate(line2):
            if i < len(lines1) and j < len(lines1[i]):
                char1 = lines1[i][j]
                if char2 != char1:
                    if char1 == ' ':
                        continue
                    highlighted_indices.append((i, j))
            elif i < len(lines1) and len(lines1[i]) <= j:
                highlighted_indices.append((i, j))
            else:
                highlighted_indices.append((i, j))

    return highlighted_indices

def compare_text(event=None):
    text1 = text_box1.get("1.0", "end-1c")
    text2 = text_box2.get("1.0", "end-1c")

    highlighted_indices = highlight_differences(text1, text2)

    text_box2.tag_remove("highlight", "1.0", "end")

    for index in highlighted_indices:
        start_pos = f"{index[0]+1}.{index[1]}"
        end_pos = f"{index[0]+1}.{index[1] + 1}"
        text_box2.tag_add("highlight", start_pos, end_pos)
        text_box2.tag_config("highlight", foreground="red")

def save_file():
    content = text_box2.get("1.0", "end-1c")
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        if os.path.exists(file_path):
            overwrite = tk.messagebox.askyesno("File Exists", "The file already exists. Do you want to overwrite it?")
            if not overwrite:
                return
        with open(file_path, "w") as file:
            file.write(content)

def update_text_box_size(event=None):
    root.after_cancel(root.after_id)
    root.after_id = root.after(200, resize_text_boxes)

def resize_text_boxes():
    width = (root.winfo_width() - 30) // 2
    text_box1.config(width=width)
    text_box2.config(width=width)

# Create the main window
root = tk.Tk()
root.title("Text Comparison App")
root.configure(bg="#6B7B8C")  # Light navy blue background color

# Calculate screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window size
window_width = int(screen_width * 0.8)
window_height = int(screen_height * 0.8)
root.geometry(f"{window_width}x{window_height}")

# Bind the update_text_box_size function to the window resize event
root.bind("<Configure>", update_text_box_size)
root.after_id = None

# Create a "Save" button
save_button = tk.Button(root, text="Save", command=save_file)
save_button.pack(fill="x", padx=5, pady=5)

# Create text entry boxes
text_box_frame1 = tk.Frame(root, bg="#6B7B8C")
text_box_frame1.pack(side="left", padx=5, pady=5, expand=True, fill="both")
text_box1 = tk.Text(text_box_frame1, height=20, bg="white", wrap=tk.WORD)  # Word wrapping
text_box1.pack(side="left", expand=True, fill="both")

text_box_frame2 = tk.Frame(root, bg="#6B7B8C")
text_box_frame2.pack(side="left", padx=5, pady=5, expand=True, fill="both")
text_box2 = tk.Text(text_box_frame2, height=20, bg="white", wrap=tk.WORD)  # Word wrapping
text_box2.pack(side="left", expand=True, fill="both")

# Bind the compare_text function to the text boxes
text_box1.bind("<KeyRelease>", compare_text)
text_box2.bind("<KeyRelease>", compare_text)

root.mainloop()
