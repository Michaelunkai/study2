import os
import pickle

class ChatbotList:
    def __init__(self):
        self.file_path = "chatbot_list.pkl"
        self.my_list = self.load_list()
        self.mission_number = len(self.my_list) + 1  # Initialize mission number

    def show_list(self):
        if not self.my_list:
            print("List is empty.")
        else:
            print("Current List:")
            for i, item in enumerate(self.my_list, start=1):
                print(f"{i}. {item}")

    def add_item(self, item):
        self.my_list.append(f"{self.mission_number}. {item}")
        self.mission_number += 1
        self.save_list()
        self.show_list()

    def remove_item(self, item_number):
        if 1 <= item_number <= len(self.my_list):
            removed_item = self.my_list.pop(item_number - 1)
            print(f"Removed {removed_item} from the list.")
            self.save_list()
            self.show_list()
        else:
            print("Invalid item number. Please try again.")

    def clear_list(self):
        self.my_list = []
        self.mission_number = 1
        print("List cleared.")
        self.save_list()

    def save_list(self):
        with open(self.file_path, "wb") as file:
            pickle.dump(self.my_list, file)

    def load_list(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "rb") as file:
                return pickle.load(file)
        else:
            return []

# Example usage
chatbot = ChatbotList()

while True:
    action = input("Enter action (add/remove/clear/show/exit): ").lower()

    if action == "exit":
        print("Exiting chatbot.")
        break
    elif action == "add":
        item = input("Enter item to add: ")
        chatbot.add_item(item)
    elif action == "remove":
        item_number = int(input("Enter item number to remove: "))
        chatbot.remove_item(item_number)
    elif action == "clear":
        chatbot.clear_list()
    elif action == "show":
        chatbot.show_list()
    else:
        print("Invalid action. Please try again.")
