import os
import pickle
import tkinter as tk
from tkinter import simpledialog, font

class ChatbotListGUI:
    def __init__(self):
        self.file_path = "chatbot_list.pkl"
        self.my_list = self.load_list()
        self.mission_number = len(self.my_list) + 1  # Initialize mission number

        self.root = tk.Tk()
        self.root.title("Chatbot List GUI")
        self.root.configure(bg='black')  # Set background color to black

        self.action_var = tk.StringVar(self.root)
        self.actions = ["add", "remove", "clear", "exit"]
        self.action_var.set(self.actions[0])

        # Set custom font
        custom_font = font.Font(family="Arial", size=12, weight="bold")

        self.action_menu = tk.OptionMenu(self.root, self.action_var, *self.actions)
        self.action_menu.config(bg='black', fg='white', font=custom_font)  # Set background, foreground, and font
        self.action_menu.pack()

        self.entry = tk.Entry(self.root, bg='black', fg='white', font=custom_font)  # Set background, foreground, and font
        self.entry.pack()
        self.entry.bind("<Return>", self.handle_enter)

        self.output_text = tk.Text(self.root, height=10, width=40, bg='black', fg='white', font=custom_font)  # Set background, foreground, and font
        self.output_text.pack()

        self.show_list()  # Automatically show the list on launch

    def handle_enter(self, event):
        self.handle_action()

    def handle_action(self):
        action = self.action_var.get().lower()

        if action == "exit":
            self.root.destroy()
        elif action == "add":
            item = self.entry.get()
            if item:
                self.add_item(item)
        elif action == "remove":
            item_number = int(self.entry.get())
            self.remove_item(item_number)
        elif action == "clear":
            self.clear_list()
        else:
            self.output_text.insert(tk.END, "Invalid action. Please try again.\n")

        self.entry.delete(0, tk.END)  # Clear the entry field after each action

    def show_list(self):
        self.output_text.delete(1.0, tk.END)  # Clear previous content
        if not self.my_list:
            self.output_text.insert(tk.END, "List is empty.\n")
        else:
            self.output_text.insert(tk.END, "Current List:\n")
            unique_numbers = set()
            for item in self.my_list:
                number, item_text = item.split('. ', 1)
                if number not in unique_numbers:
                    self.output_text.insert(tk.END, f"{item}\n")
                    unique_numbers.add(number)

    def add_item(self, item):
        self.my_list.append(f"{self.mission_number}. {item}")
        self.mission_number += 1
        self.save_list()
        self.show_list()

    def remove_item(self, item_number):
        if 1 <= item_number <= len(self.my_list):
            removed_item = self.my_list.pop(item_number - 1)
            self.output_text.insert(tk.END, f"Removed {removed_item} from the list.\n")
            self.recalculate_numbers()
            self.save_list()
            self.show_list()
        else:
            self.output_text.insert(tk.END, "Invalid item number. Please try again.\n")

    def recalculate_numbers(self):
        unique_numbers = set()
        for i, _ in enumerate(self.my_list, start=1):
            number, item_text = self.my_list[i - 1].split('. ', 1)
            if number not in unique_numbers:
                self.my_list[i - 1] = f"{i}. {item_text}"
                unique_numbers.add(number)

    def clear_list(self):
        self.my_list = []
        self.mission_number = 1
        self.output_text.insert(tk.END, "List cleared.\n")
        self.save_list()
        self.show_list()

    def save_list(self):
        with open(self.file_path, "wb") as file:
            pickle.dump(self.my_list, file)

    def load_list(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "rb") as file:
                return pickle.load(file)
        else:
            return []

    def run(self):
        self.root.mainloop()

# Example usage
chatbot_gui = ChatbotListGUI()
chatbot_gui.run()
