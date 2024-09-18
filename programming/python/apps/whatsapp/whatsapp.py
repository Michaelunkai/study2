import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from ttkthemes import ThemedTk
from PIL import Image, ImageTk, ImageOps
import requests
from threading import Thread
from queue import Queue
from datetime import datetime
import time  # Added time module

# Green API credentials
INSTANCE_ID = "<INSTANCE_ID>"
API_TOKEN = "<API_TOKEN>"
SEND_MESSAGE_URL = f"https://api.green-api.com/waInstance{INSTANCE_ID}/SendMessage/{API_TOKEN}"

# Always use your phone number
YOUR_PHONE_NUMBER = "<YOUR_PHONE_NUMBER>"
CHAT_ID = f"{YOUR_PHONE_NUMBER}@c.us"

# Paths to save persistent data
DATA_FILE_PATH = "message_data.json"
LOG_FILE_PATH = "message_log.txt"
DRAFT_FILE_PATH = "draft_message.txt"

# Load persistent data
if os.path.exists(DATA_FILE_PATH):
    with open(DATA_FILE_PATH, "r") as file:
        data = json.load(file)
        message_count = data.get("message_count", 0)
        message_history = data.get("message_history", [])
        templates = data.get("templates", [
            "Hello!", "How are you?", "Thank you!", "Please call me back.", 
            "Good morning!", "Good night!", "I miss you.", "Let’s meet up!", 
            "Can we talk?", "I’m thinking about you.", "Where are you?", 
            "See you soon.", "Take care.", "Good luck!", "I appreciate you.",
            "You’re the best!", "Have a nice day!", "Let’s catch up.", 
            "Call me when you can.", "Can we reschedule?"
        ])
else:
    message_count = 0
    message_history = []
    templates = [
        "Hello!", "How are you?", "Thank you!", "Please call me back.", 
        "Good morning!", "Good night!", "I miss you.", "Let’s meet up!", 
        "Can we talk?", "I’m thinking about you.", "Where are you?", 
        "See you soon.", "Take care.", "Good luck!", "I appreciate you.",
        "You’re the best!", "Have a nice day!", "Let’s catch up.", 
        "Call me when you can.", "Can we reschedule?"
    ]

# Save persistent data
def save_data():
    with open(DATA_FILE_PATH, "w") as file:
        json.dump({"message_count": message_count, "message_history": message_history, "templates": templates}, file)

# Save log
def save_log(log_entry):
    with open(LOG_FILE_PATH, "a") as log_file:
        log_file.write(log_entry + "\n")

# Save draft message
def save_draft(message):
    with open(DRAFT_FILE_PATH, "w") as file:
        file.write(message)

# Load draft message
def load_draft():
    if os.path.exists(DRAFT_FILE_PATH):
        with open(DRAFT_FILE_PATH, "r") as file:
            return file.read()
    return ""

# Define the main application class
class GreenAPIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WhatsApp Messaging Service")
        self.queue = Queue()
        self.current_theme = "dark"
        self.apply_theme(self.current_theme)
        self.root.geometry("600x500")  # Adjusted window size for button fit

        # App title with Lobster font
        self.title_label = tk.Label(root, text="WhatsApp Messaging Service", bg=self.bg_color, fg=self.text_color, font=("Lobster", 24, "bold"))
        self.title_label.pack(pady=10)

        # WhatsApp logo without white border and 2x size
        logo_image = Image.open(r"C:\study\programming\APIs\greenapi\whatsapp.jpeg")  # Use your path to the logo image
        logo_image = ImageOps.contain(logo_image, (120, 120))  # Double size
        self.logo = ImageTk.PhotoImage(logo_image)
        self.logo_label = tk.Label(root, image=self.logo, bg=self.bg_color)
        self.logo_label.pack(pady=5)

        # Message counter display
        self.counter_label = tk.Label(root, text=f"Messages Sent: {message_count}", bg=self.bg_color, fg=self.text_color, font=("Lobster", 14, "bold"))
        self.counter_label.pack(pady=5)

        # Message entry box with Lobster font in the middle
        self.message_label = tk.Label(root, text="Message:", bg=self.bg_color, fg=self.text_color, font=("Lobster", 14, "bold"))
        self.message_label.pack(pady=5)
        
        self.message_text = tk.Text(root, height=5, width=40, bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.entry_fg, font=("Lobster", 14, "bold"))
        self.message_text.pack(pady=5)

        # Buttons area
        self.button_frame = tk.Frame(root, bg=self.bg_color)
        self.button_frame.pack(pady=5)

        # Buttons
        self.send_button = self.create_button(self.button_frame, "Send", self.send_message)
        self.send_button.grid(row=0, column=0, padx=5, pady=5)

        self.resend_button = self.create_button(self.button_frame, "Resend", self.resend_message)
        self.resend_button.grid(row=0, column=1, padx=5, pady=5)

        self.schedule_button = self.create_button(self.button_frame, "Schedule", self.schedule_message)
        self.schedule_button.grid(row=0, column=2, padx=5, pady=5)

        self.save_draft_button = self.create_button(self.button_frame, "Save Draft", self.save_draft_action)
        self.save_draft_button.grid(row=0, column=3, padx=5, pady=5)

        self.load_draft_button = self.create_button(self.button_frame, "Load Draft", self.load_draft_action)
        self.load_draft_button.grid(row=0, column=4, padx=5, pady=5)

        self.manage_templates_button = self.create_button(self.button_frame, "Templates", self.manage_templates)
        self.manage_templates_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.clear_button = self.create_button(self.button_frame, "Clear", self.clear_message)
        self.clear_button.grid(row=1, column=2, padx=5, pady=5)

        self.toggle_theme_button = self.create_button(self.button_frame, "Dark/Light", self.toggle_theme)
        self.toggle_theme_button.grid(row=1, column=3, columnspan=2, padx=5, pady=5)

        # Delivery status display
        self.status_label = tk.Label(root, text="", bg=self.bg_color, fg=self.text_color, font=("Lobster", 14, "bold"))
        self.status_label.pack(pady=5)

        # Character and word counters
        self.char_count_label = tk.Label(root, text="Characters: 0", bg=self.bg_color, fg=self.text_color, font=("Lobster", 14, "bold"))
        self.char_count_label.pack(pady=5)

        self.word_count_label = tk.Label(root, text="Words: 0", bg=self.bg_color, fg=self.text_color, font=("Lobster", 14, "bold"))
        self.word_count_label.pack(pady=5)

        self.message_text.bind("<KeyRelease>", self.update_counters)

        # Keyboard shortcuts
        root.bind("<Control-s>", lambda event: self.send_message())
        root.bind("<Control-l>", lambda event: self.clear_message())

    def apply_theme(self, theme):
        if theme == "dark":
            self.bg_color = "#000000"
            self.text_color = "white"
            self.entry_bg = "#333333"
            self.entry_fg = "white"
        else:
            self.bg_color = "#1E4F32"  # Dark green
            self.text_color = "white"
            self.entry_bg = "#E8F5E9"
            self.entry_fg = "black"
        self.root.configure(bg=self.bg_color)

    def create_button(self, parent, text, command):
        style = ttk.Style()
        style.configure("W.TButton", font=("Lobster", 12, "bold"), foreground="white", background="black")
        button = ttk.Button(parent, text=text, command=command, style="W.TButton")
        button.grid_configure(padx=5, pady=5)  # Ensure even padding
        return button

    def update_widgets(self):
        self.title_label.configure(bg=self.bg_color, fg=self.text_color)
        self.logo_label.configure(bg=self.bg_color)
        self.counter_label.configure(bg=self.bg_color, fg=self.text_color)
        self.message_label.configure(bg=self.bg_color, fg=self.text_color)
        self.message_text.configure(bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.entry_fg)
        self.status_label.configure(bg=self.bg_color, fg=self.text_color)
        self.char_count_label.configure(bg=self.bg_color, fg=self.text_color)
        self.word_count_label.configure(bg=self.bg_color, fg=self.text_color)

    def use_template(self, event):
        selected_template = self.template_var.get()
        self.message_text.delete("1.0", tk.END)
        self.message_text.insert(tk.END, selected_template)

    def send_message(self):
        global message_count, last_message, message_history

        message = self.message_text.get("1.0", tk.END).strip()

        if not message:
            messagebox.showerror("Error", "Message cannot be empty.")
            return

        last_message = message  # Save the last message sent

        # Start thread to send the message
        Thread(target=self._send_message_thread, args=(CHAT_ID, message)).start()

    def resend_message(self):
        global last_message

        if not last_message:
            messagebox.showinfo("Info", "No message to resend.")
            return

        # Start thread to resend the last message
        Thread(target=self._send_message_thread, args=(CHAT_ID, last_message)).start()

    def clear_message(self):
        self.message_text.delete("1.0", tk.END)
        self.status_label.config(text="Message cleared.")

    def schedule_message(self):
        message = self.message_text.get("1.0", tk.END).strip()

        if not message:
            messagebox.showerror("Error", "Message cannot be empty.")
            return

        # Get the number of times to send the message
        repeat_times = simpledialog.askinteger("Input", "How many times to send the message?")

        if repeat_times is None or repeat_times <= 0:
            return

        # Get the time interval in seconds
        interval_seconds = simpledialog.askinteger("Input", "Enter time interval in seconds:")

        if interval_seconds is None or interval_seconds <= 0:
            return

        # Start thread to schedule the message
        Thread(target=self._schedule_message_thread, args=(CHAT_ID, message, repeat_times, interval_seconds)).start()

    def _send_message_thread(self, chat_id, message):
        global message_count, message_history

        payload = {
            "chatId": chat_id,
            "message": message
        }

        response = requests.post(SEND_MESSAGE_URL, json=payload)

        if response.status_code == 200:
            message_count += 1
            message_history.append({"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "message": message})
            save_data()
            log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Sent: {message}"
            save_log(log_entry)
            self.queue.put("Message sent successfully!")
            self.status_label.config(text="Message sent successfully!")

        else:
            self.queue.put("Failed to send message.")
            self.status_label.config(text="Failed to send message.")

        # Update the message counter
        self.counter_label.config(text=f"Messages Sent: {message_count}")

    def _schedule_message_thread(self, chat_id, message, repeat_times, interval_seconds):
        for _ in range(repeat_times):
            self._send_message_thread(chat_id, message)
            time.sleep(interval_seconds)

    def save_draft_action(self):
        message = self.message_text.get("1.0", tk.END).strip()
        save_draft(message)
        self.status_label.config(text="Draft saved successfully.")

    def load_draft_action(self):
        draft_message = load_draft()
        if draft_message:
            self.message_text.delete("1.0", tk.END)
            self.message_text.insert(tk.END, draft_message)
            self.status_label.config(text="Draft loaded successfully.")
        else:
            self.status_label.config(text="No draft to load.")

    def manage_templates(self):
        self.manage_window = tk.Toplevel(self.root)
        self.manage_window.title("Manage Templates")
        self.manage_window.configure(bg=self.bg_color)

        def add_template():
            new_template = simpledialog.askstring("New Template", "Enter the new template:")
            if new_template:
                templates.append(new_template)
                save_data()
                self.update_template_list()

        def edit_template():
            selected_index = self.template_listbox.curselection()
            if not selected_index:
                messagebox.showinfo("Info", "Select a template to edit.")
                return
            new_template = simpledialog.askstring("Edit Template", "Edit the template:", initialvalue=templates[selected_index[0]])
            if new_template:
                templates[selected_index[0]] = new_template
                save_data()
                self.update_template_list()

        def delete_template():
            selected_index = self.template_listbox.curselection()
            if not selected_index:
                messagebox.showinfo("Info", "Select a template to delete.")
                return
            del templates[selected_index[0]]
            save_data()
            self.update_template_list()

        self.template_listbox = tk.Listbox(self.manage_window, font=("Lobster", 14), bg=self.entry_bg, fg=self.entry_fg)
        self.template_listbox.pack(fill="both", expand=True)

        self.update_template_list()

        button_frame = tk.Frame(self.manage_window, bg=self.bg_color)
        button_frame.pack(pady=10)

        add_button = self.create_button(button_frame, "Add", add_template)
        add_button.pack(side="left", padx=5, pady=5)

        edit_button = self.create_button(button_frame, "Edit", edit_template)
        edit_button.pack(side="left", padx=5, pady=5)

        delete_button = self.create_button(button_frame, "Delete", delete_template)
        delete_button.pack(side="left", padx=5, pady=5)

        send_button = self.create_button(button_frame, "Send", self.send_template_message)
        send_button.pack(side="left", padx=5, pady=5)

    def update_template_list(self):
        self.template_listbox.delete(0, tk.END)
        for template in templates:
            self.template_listbox.insert(tk.END, template)

    def send_template_message(self):
        selected_index = self.template_listbox.curselection()
        if not selected_index:
            messagebox.showinfo("Info", "Select a template to send.")
            return
        message = templates[selected_index[0]]
        self.message_text.delete("1.0", tk.END)
        self.message_text.insert(tk.END, message)
        self.send_message()

    def toggle_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.apply_theme(self.current_theme)
        self.update_widgets()

    def update_counters(self, event=None):
        message = self.message_text.get("1.0", tk.END).strip()
        char_count = len(message)
        word_count = len(message.split())
        self.char_count_label.config(text=f"Characters: {char_count}")
        self.word_count_label.config(text=f"Words: {word_count}")

# Main function to run the application
def main():
    root = ThemedTk(theme="equilux")  # Dark theme
    app = GreenAPIApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
