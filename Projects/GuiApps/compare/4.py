import tkinter as tk

def compare_texts():
    text1 = text_box1.get("1.0", "end-1c").splitlines()
    text2 = text_box2.get("1.0", "end-1c").splitlines()

    # Clear any previous highlighting
    text_box1.tag_remove("highlight", "1.0", "end")
    text_box2.tag_remove("highlight", "1.0", "end")

    # Find differences line by line and mark them
    for i, (line1, line2) in enumerate(zip(text1, text2), start=1):
        for j, (char1, char2) in enumerate(zip(line1, line2)):
            # Mark differences in window 1 (text_box1) in red
            if char1 != char2:
                index = f"{i}.{j}"
                text_box1.tag_add("highlight", index, f"{index}+1c")
        
        # Mark differences in window 2 (text_box2) in purple
        # If one line is longer than the other, mark the extra part in purple
        if line1 != line2:
            text_box2.tag_add("highlight", f"{i}.0", f"{i}.{len(line2)}")
    
    text_box1.tag_config("highlight", foreground="red")
    text_box2.tag_config("highlight", foreground="purple")

# Create the main window
root = tk.Tk()
root.title("Text Comparator")

# Create text boxes
text_box1 = tk.Text(root, height=30, width=60, font=("Arial", 12, "bold"))
text_box1.pack(side=tk.LEFT, padx=5, pady=5)

text_box2 = tk.Text(root, height=30, width=60, font=("Arial", 12, "bold"))
text_box2.pack(side=tk.RIGHT, padx=5, pady=5)

# Create compare button
compare_button = tk.Button(root, text="Compare", command=compare_texts)
compare_button.pack()

# Run the application
root.mainloop()
