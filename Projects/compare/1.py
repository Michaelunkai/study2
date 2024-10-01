import difflib
import tkinter as tk

def highlight_differences(text1, text2):
    differ = difflib.Differ()
    diff = list(differ.compare(text1.splitlines(), text2.splitlines()))
    highlighted_text = ""

    line_num1 = 1
    line_num2 = 1

    for line in diff:
        if line.startswith('?'):  # Skip diff indication lines
            continue
        elif line.startswith('+') or line.startswith('-'):
            highlighted_text += f'\nLine {line_num1} (Text 1): ' + line.strip()
            highlighted_text += f'\nLine {line_num2} (Text 2): ' + line.strip()
        
        # Increment line numbers for both text boxes
        if line[0] != '+':
            line_num1 += 1
        if line[0] != '-':
            line_num2 += 1
    
    return highlighted_text.strip()

def compare_text():
    text1 = text_box1.get("1.0", "end-1c")
    text2 = text_box2.get("1.0", "end-1c")
    
    highlighted_text = highlight_differences(text1, text2)
    
    compared_text.delete("1.0", "end")
    compared_text.insert("1.0", highlighted_text)

def search_text(text_box, search_entry):
    # Clear previous search highlights
    text_box.tag_remove("search", "1.0", "end")

    query = search_entry.get()
    if query:
        start_pos = "1.0"
        while True:
            start_pos = text_box.search(query, start_pos, stopindex="end", nocase=True)
            if not start_pos:
                break
            end_pos = f"{start_pos}+{len(query)}c"
            text_box.tag_add("search", start_pos, end_pos)
            start_pos = end_pos
        text_box.tag_config("search", background="yellow")

# Create the main window
root = tk.Tk()
root.title("Text Comparison App")
root.configure(bg="#6B7B8C")  # Light navy blue background color

# Create text entry boxes
text_box_frame1 = tk.Frame(root, bg="#6B7B8C")
text_box_frame1.pack(side="left", padx=5, pady=5)
text_box1 = tk.Text(text_box_frame1, height=40, width=55, bg="white", wrap=tk.WORD)  # Word wrapping
text_box1.pack(side="top")

text_box_frame2 = tk.Frame(root, bg="#6B7B8C")
text_box_frame2.pack(side="left", padx=5, pady=5)
text_box2 = tk.Text(text_box_frame2, height=40, width=55, bg="white", wrap=tk.WORD)  # Word wrapping
text_box2.pack(side="top")

# Create search boxes
search_frame1 = tk.Frame(root, bg="#6B7B8C")
search_frame1.pack(side="top", fill="x")
search_entry1 = tk.Entry(search_frame1)
search_entry1.pack(side="left", padx=(5, 2), pady=5)
search_button1 = tk.Button(search_frame1, text="Search", command=lambda: search_text(text_box1, search_entry1))
search_button1.pack(side="left", padx=(0, 5), pady=5)

search_frame2 = tk.Frame(root, bg="#6B7B8C")
search_frame2.pack(side="top", fill="x")
search_entry2 = tk.Entry(search_frame2)
search_entry2.pack(side="left", padx=(5, 2), pady=5)
search_button2 = tk.Button(search_frame2, text="Search", command=lambda: search_text(text_box2, search_entry2))
search_button2.pack(side="left", padx=(0, 5), pady=5)

# Create compare button
compare_button = tk.Button(root, text="Compare", command=compare_text, bg="#4CAF50", fg="white")  # Green button
compare_button.pack(fill="x", padx=5, pady=5)

# Create text box for compared text
compared_text = tk.Text(root, height=30, width=40, bg="white")
compared_text.pack(fill="both", expand=True, padx=5, pady=5)

root.mainloop()
