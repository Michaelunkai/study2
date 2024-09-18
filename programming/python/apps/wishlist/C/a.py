import sqlite3
import tkinter as tk
from tkinter import messagebox
import subprocess

# Connect to SQLite database or create it if it doesn't exist
conn = sqlite3.connect('wishlist.db')

# Create a cursor object
cursor = conn.cursor()

# Define SQL queries to create tables for movies, TV shows, games, and anime
create_movies_table = """CREATE TABLE IF NOT EXISTS movies (
                            id INTEGER PRIMARY KEY,
                            title TEXT
                        )"""

create_tv_shows_table = """CREATE TABLE IF NOT EXISTS tv_shows (
                                id INTEGER PRIMARY KEY,
                                title TEXT
                            )"""

create_games_table = """CREATE TABLE IF NOT EXISTS games (
                            id INTEGER PRIMARY KEY,
                            title TEXT
                        )"""

create_anime_table = """CREATE TABLE IF NOT EXISTS anime (
                            id INTEGER PRIMARY KEY,
                            title TEXT
                        )"""

# Execute SQL queries to create tables
cursor.execute(create_movies_table)
cursor.execute(create_tv_shows_table)
cursor.execute(create_games_table)
cursor.execute(create_anime_table)

# Commit changes to the database
conn.commit()

# Function to add a new item to a category
def add_item(category, entry_widget):
    titles = entry_widget.get("1.0", "end").split('\n')
    for title in titles:
        if title.strip():
            cursor.execute(f"INSERT INTO {category} (title) VALUES (?)", (title.strip(),))
    conn.commit()
    refresh_items_list(category, listbox_widgets[category])
    messagebox.showinfo("Success", f"{category.capitalize()}(s) added successfully!")

# Function to delete all listings from a category
def delete_listings(category):
    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete all {category.replace('_', ' ')}?")
    if confirm:
        cursor.execute(f"DELETE FROM {category}")
        conn.commit()
        refresh_items_list(category, listbox_widgets[category])
        messagebox.showinfo("Success", f"All {category.replace('_', ' ')} deleted successfully.")

# Function to delete selected items
def delete_selected_items(category, listbox_widget):
    selected_indices = listbox_widget.curselection()
    if selected_indices:
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected item(s)?")
        if confirm:
            for index in selected_indices:
                item_id = items_ids[category][index]
                cursor.execute(f"DELETE FROM {category} WHERE id=?", (item_id,))
            conn.commit()
            refresh_items_list(category, listbox_widget)
            messagebox.showinfo("Success", "Selected item(s) deleted successfully.")
    else:
        messagebox.showerror("Error", "No items selected for deletion.")

# Function to refresh items list
def refresh_items_list(category, listbox_widget):
    listbox_widget.delete(0, tk.END)
    items_ids[category] = []
    cursor.execute(f"SELECT * FROM {category}")
    items = cursor.fetchall()
    for item in items:
        item_id = item[0]
        title = item[1]
        listbox_widget.insert(tk.END, title)
        items_ids[category].append(item_id)

# Function to mark an item
def mark_item(event, listbox_widget):
    item_index = listbox_widget.nearest(event.y)
    if item_index not in marked_items:
        marked_items.add(item_index)
        listbox_widget.itemconfig(item_index, bg="blue")
    else:
        marked_items.remove(item_index)
        listbox_widget.itemconfig(item_index, bg="white")

# Function to show context menu
def show_context_menu(event, listbox_widget):
    global marked_items
    selected_items = [listbox_widget.get(i) for i in marked_items]
    if selected_items:
        copied_text = "\n".join(selected_items)
        listbox_widget.clipboard_clear()
        listbox_widget.clipboard_append(copied_text)

# Function to search and download selected titles
def search_and_download():
    global marked_items
    selected_titles = []
    for category, listbox_widget in listbox_widgets.items():
        selected_indices = listbox_widget.curselection()
        for index in selected_indices:
            selected_titles.append((category, listbox_widget.get(index)))
    if not selected_titles:
        return  # No titles selected

    # Group titles by category
    categories_dict = {}
    for category, title in selected_titles:
        if category not in categories_dict:
            categories_dict[category] = []
        categories_dict[category].append(title)

    # Download titles from each category one after the other
    for category, titles in categories_dict.items():
        for title in titles:
            try:
                if category == "tv_shows":
                    title += " s01"
                elif category == "anime":
                    title += " dual audio"
                elif category == "movies":
                    title += " 1080p"
                title_with_quotes = f'"{title}"'
                command = ["python", "-m", "1337x", "-s", "SEEDERS", title_with_quotes]
                subprocess.run(["powershell", "-c", " ".join(command)], check=True)  # Open PowerShell and run command
            except subprocess.CalledProcessError:
                pass  # Ignore invalid choice

    # Clear marked items after download
    marked_items.clear()

# Function to view wishlist items
def view_wishlist():
    global listbox_widgets  # To make it accessible outside the function
    global marked_items

    # Create a new window for displaying wishlist items
    view_window = tk.Toplevel(root)
    view_window.title("View Wishlist")
    view_window.configure(background="black")

    # Set the width and height of the view window
    view_window_width = 1000
    view_window_height = 600
    view_window.geometry(f"{view_window_width}x{view_window_height}")

    # Calculate the width for each listbox frame
    frame_width = (view_window_width - 60) // 4

    def remove_all_items(category, listbox_widget):
        confirm = messagebox.askyesno("Confirm Remove All", f"Are you sure you want to remove all {category.replace('_', ' ')}?")
        if confirm:
            cursor.execute(f"DELETE FROM {category}")
            conn.commit()
            refresh_items_list(category, listbox_widget)
            messagebox.showinfo("Success", f"All {category.replace('_', ' ')} removed successfully.")

    categories = ["movies", "tv_shows", "games", "anime"]
    listbox_widgets = {}
    marked_items = set()

    for index, category in enumerate(categories):
        # Create a frame for each category
        category_frame = tk.Frame(view_window, bg="black", width=frame_width)
        category_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Query items for the category
        cursor.execute(f"SELECT * FROM {category}")
        items = cursor.fetchall()
        if items:
            category_label = tk.Label(category_frame, text=category.capitalize(), font=("Helvetica", 16, "bold"), fg="red", bg="black")
            category_label.pack()
            category_list = tk.Listbox(category_frame, height=20, width=30, bg="white", fg="black", selectmode=tk.MULTIPLE)
            for item in items:
                category_list.insert(tk.END, item[1])
            category_list.pack(fill=tk.BOTH, expand=True)
            category_scroll = tk.Scrollbar(category_frame, orient=tk.VERTICAL)
            category_scroll.config(command=category_list.yview)
            category_scroll.pack(side=tk.RIGHT, fill=tk.Y)
            category_list.config(yscrollcommand=category_scroll.set)
            category_list.bind("<Button-1>", lambda event, listbox=category_list: mark_item(event, listbox))
            listbox_widgets[category] = category_list
            refresh_items_list(category, category_list)

            # Create Remove All button for each category
            remove_button = tk.Button(category_frame, text="Remove All", command=lambda cat=category, listbox=category_list: remove_all_items(cat, listbox), font=("Helvetica", 10), fg="red", bg="black")
            remove_button.pack(pady=5)

            # Create Remove Selected button for each category
            delete_selected_button = tk.Button(category_frame, text="Remove Selected", command=lambda cat=category, listbox=category_list: delete_selected_items(cat, listbox), font=("Helvetica", 10), fg="red", bg="black")
            delete_selected_button.pack(pady=5)
        else:
            category_label = tk.Label(category_frame, text=f"No {category.replace('_', ' ')} found", bg="black", fg="white")
            category_label.pack()

    # Create Search & Download button
    download_button = tk.Button(view_window, text="Search & Download", command=search_and_download, font=("Helvetica", 12, "bold"), fg="blue", bg="black")
    download_button.pack(pady=10)

    # Bind right-click to show context menu
    for listbox_widget in listbox_widgets.values():
        listbox_widget.bind("<Button-3>", lambda event, widget=listbox_widget: show_context_menu(event, widget))
        listbox_widget.bind("<Return>", lambda event: search_and_download())

# Function to paste items into a category
def paste_items(entry_widget):
    try:
        pasted_text = root.clipboard_get()
        entry_widget.insert(tk.END, pasted_text)
    except tk.TclError:
        messagebox.showerror("Error", "Clipboard is empty!")

# Function to create a context menu with a paste option
def create_context_menu(entry_widget):
    context_menu = tk.Menu(root, tearoff=0)
    context_menu.add_command(label="Paste", command=lambda: paste_items(entry_widget))
    def show_context_menu(event):
        context_menu.tk_popup(event.x_root, event.y_root)
    entry_widget.bind("<Button-3>", show_context_menu)

# Main window
root = tk.Tk()
root.title("Michael Fedro's Wishlist Manager")
root.configure(background="black")

# Labels
labels = ["Movie(s):", "TV Show(s):", "Game(s):", "Anime(s):"]
for i, label_text in enumerate(labels):
    label = tk.Label(root, text=label_text, font=("Helvetica", 12, "bold"), fg="red", bg="black")
    label.grid(row=i, column=0, padx=5, pady=5, sticky="w")

# Entry widgets
entry_widgets = {}
for i, category in enumerate(["movies", "tv_shows", "games", "anime"]):
    entry_widget = tk.Text(root, height=5, width=30)
    entry_widget.grid(row=i, column=1, padx=5, pady=5)
    entry_widgets[category] = entry_widget
    create_context_menu(entry_widget)  # Add context menu to entry widget

# Buttons to add items
add_buttons = {}
for i, category in enumerate(["movies", "tv_shows", "games", "anime"]):
    add_button = tk.Button(root, text=f"Add {category.capitalize()}", width=15, command=lambda cat=category, entry=entry_widgets[category]: add_item(cat, entry))
    add_button.grid(row=i, column=2, padx=5, pady=5, sticky="w")
    add_buttons[category] = add_button

# View button
view_button = tk.Button(root, text="See Wishlist", command=view_wishlist, font=("Helvetica", 12, "bold"), fg="red", bg="black")
view_button.grid(row=4, column=0, columnspan=3, pady=10, sticky="we")

# Dictionary to hold item ids for each category
items_ids = {}

# Start the GUI
root.mainloop()

# Close the database connection
conn.close()
