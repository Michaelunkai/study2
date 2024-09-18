import tkinter as tk
from tkinter import ttk
import os

class StickyNoteApp:
    def __init__(self, master):
        self.master = master
        master.title("NoteHub by Misha Fedro")
        master.geometry("1000x600")

        # Custom color scheme
        master.configure(bg='#000000')  # Set background color to black

        style = ttk.Style()
        style.configure("TEntry", padding=10, relief="flat", background='#FF0000', foreground='#000000', font=('Arial', 14))
        style.configure("TButton", padding=10, relief="flat", background='#FF0000', foreground='#000000', font=('Arial', 12))

        self.note_entry = ttk.Entry(master, width=50, style="TEntry")  # Themed Entry widget
        self.note_entry.pack(pady=10)
        self.note_entry.bind("<Return>", self.add_note_on_enter)

        button_frame = tk.Frame(master, bg='#2E2E2E')  # Frame to contain buttons
        button_frame.pack()

        self.add_button = ttk.Button(button_frame, text="Add Sticky Note", command=self.add_note, style="TButton")  # Themed Button widget
        self.add_button.pack(side=tk.LEFT)

        self.refresh_button = ttk.Button(button_frame, text="Refresh", command=self.refresh_notes, style="TButton")
        self.refresh_button.pack(side=tk.LEFT, padx=5)

        self.notes_frame = tk.Frame(master, bg='#2E2E2E')  # Frame to contain notes
        self.notes_frame.pack(expand=True, fill=tk.BOTH)

        self.notes = []
        self.load_notes()

        self.populate_notes_frame()

        master.protocol("WM_DELETE_WINDOW", self.on_close)

    def add_note(self, event=None):
        note_text = self.note_entry.get()
        if note_text:
            self.notes.append(note_text)
            self.note_entry.delete(0, tk.END)
            self.save_notes()
            self.populate_notes_frame()

    def add_note_on_enter(self, event):
        self.add_note()

    def populate_notes_frame(self):
        for widget in self.notes_frame.winfo_children():
            widget.destroy()

        for note in self.notes:
            note_frame = tk.Frame(self.notes_frame, bg='#2E2E2E')  # Frame for each note
            note_frame.pack(pady=10, fill=tk.X)

            note_label = tk.Label(note_frame, text=note, bg='#2E2E2E', fg='#FF0000', font=('Arial', 16, 'bold'))  # Label for note
            note_label.pack(side=tk.LEFT, padx=10)

            copy_button = ttk.Button(note_frame, text="Copy", command=lambda n=note: self.copy_note(n), style="TButton")  # Copy button for each note
            copy_button.pack(side=tk.RIGHT)

            delete_button = ttk.Button(note_frame, text="Remove", command=lambda n=note: self.remove_note(n, note_frame), style="TButton")  # Remove button for each note
            delete_button.pack(side=tk.RIGHT)

    def copy_note(self, note):
        self.master.clipboard_clear()
        self.master.clipboard_append(note)
        self.master.update()

    def remove_note(self, note, frame):
        if note in self.notes:
            self.notes.remove(note)
            self.save_notes()
            frame.destroy()
        else:
            print(f"Note '{note}' not found in the list.")

    def save_notes(self):
        file_path = os.path.join(os.path.expanduser('~'), "sticky_notes.txt")
        with open(file_path, "w") as file:
            for note in self.notes:
                file.write(note + "\n")

    def load_notes(self):
        file_path = os.path.join(os.path.expanduser('~'), "sticky_notes.txt")
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                self.notes = [line.strip() for line in file.readlines()]

    def refresh_notes(self):
        self.load_notes()
        self.populate_notes_frame()

    def on_close(self):
        self.save_notes()
        self.master.destroy()

def run_sticky_note_app():
    root = tk.Tk()
    app = StickyNoteApp(root)
    root.mainloop()

if __name__ == "__main__":
    run_sticky_note_app()
