import sqlite3
import tkinter as tk
from tkinter import messagebox
import subprocess
import paramiko
import os
import tempfile
import sys
import shutil

# -------------------------------
# Configuration and file settings
# -------------------------------
# SSH connection details
HOSTNAME = '54.173.176.93'
USERNAME = 'ubuntu'
KEY_PATH = r"C:\backup\windowsapps\Credentials\AWS\key.pem"
REMOTE_DB_PATH = '/home/ubuntu/wishlist/wishlist.db'

# Local database file name
LOCAL_DB_FILENAME = "wishlist.db"

# ----------------------------------------
# Remote sync functions using Paramiko/SFTP
# ----------------------------------------
def download_remote_db():
    """Download the remote database and save it as the local database file."""
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=HOSTNAME, username=USERNAME, key_filename=KEY_PATH)
        
        sftp = ssh.open_sftp()
        local_temp_path = os.path.join(tempfile.gettempdir(), 'wishlist_remote.db')
        sftp.get(REMOTE_DB_PATH, local_temp_path)
        
        sftp.close()
        ssh.close()
        
        # Copy downloaded file to the local working directory.
        shutil.copy(local_temp_path, LOCAL_DB_FILENAME)
        return LOCAL_DB_FILENAME
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download remote database: {str(e)}")
        sys.exit(1)

def upload_remote_db():
    """Upload the current local database file to the remote location."""
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=HOSTNAME, username=USERNAME, key_filename=KEY_PATH)
        
        sftp = ssh.open_sftp()
        sftp.put(LOCAL_DB_FILENAME, REMOTE_DB_PATH)
        
        sftp.close()
        ssh.close()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to upload database: {str(e)}")

# ----------------------------------------
# Database initialization
# ----------------------------------------
def init_local_db():
    """Initialize the local SQLite database.
       If the database file doesn't exist, try to download it from the remote.
       Then create tables if they don't exist.
    """
    if not os.path.exists(LOCAL_DB_FILENAME):
        download_remote_db()
    
    conn = sqlite3.connect(LOCAL_DB_FILENAME)
    cursor = conn.cursor()
    
    tables = {
        "movies": "CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY, title TEXT)",
        "tv_shows": "CREATE TABLE IF NOT EXISTS tv_shows (id INTEGER PRIMARY KEY, title TEXT)",
        "games": "CREATE TABLE IF NOT EXISTS games (id INTEGER PRIMARY KEY, title TEXT)",
        "anime": "CREATE TABLE IF NOT EXISTS anime (id INTEGER PRIMARY KEY, title TEXT)"
    }
    
    for table_name, create_sql in tables.items():
        cursor.execute(create_sql)
    
    conn.commit()
    return conn, cursor

# Initialize the database
conn, cursor = init_local_db()

# Dictionaries and sets for managing the GUI
categories = ["movies", "tv_shows", "games", "anime"]
items_ids = {category: [] for category in categories}
listbox_widgets = {}
marked_items = set()

# ----------------------------------------
# GUI Functions
# ----------------------------------------
def add_item(category, entry_widget):
    titles = entry_widget.get("1.0", "end-1c").split('\n')
    for title in titles:
        if title.strip():
            cursor.execute(f"INSERT INTO {category} (title) VALUES (?)", (title.strip(),))
    conn.commit()
    upload_remote_db()
    refresh_items_list(category, listbox_widgets[category])
    messagebox.showinfo("Success", f"{category.capitalize()}(s) added successfully!")
    entry_widget.delete("1.0", tk.END)

def delete_listings(category):
    if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete all {category.replace('_', ' ')}?"):
        cursor.execute(f"DELETE FROM {category}")
        conn.commit()
        upload_remote_db()
        refresh_items_list(category, listbox_widgets[category])
        messagebox.showinfo("Success", f"All {category.replace('_', ' ')} deleted successfully.")

def delete_selected_items(category, listbox_widget):
    selected_indices = listbox_widget.curselection()
    if not selected_indices:
        messagebox.showerror("Error", "No items selected for deletion.")
        return
    
    if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected item(s)?"):
        # Delete in reverse order so that indices remain valid
        for index in reversed(selected_indices):
            item_id = items_ids[category][index]
            cursor.execute(f"DELETE FROM {category} WHERE id=?", (item_id,))
        conn.commit()
        upload_remote_db()
        refresh_items_list(category, listbox_widget)
        messagebox.showinfo("Success", "Selected item(s) deleted successfully.")

def refresh_items_list(category, listbox_widget):
    listbox_widget.delete(0, tk.END)
    items_ids[category] = []
    cursor.execute(f"SELECT * FROM {category}")
    for item in cursor.fetchall():
        listbox_widget.insert(tk.END, item[1])
        items_ids[category].append(item[0])

def mark_item(event, listbox_widget):
    item_index = listbox_widget.nearest(event.y)
    if item_index not in marked_items:
        marked_items.add(item_index)
        listbox_widget.itemconfig(item_index, bg="blue")
    else:
        marked_items.remove(item_index)
        listbox_widget.itemconfig(item_index, bg="white")

def show_context_menu(event, listbox_widget):
    selected_items = [listbox_widget.get(i) for i in marked_items]
    if selected_items:
        copied_text = "\n".join(selected_items)
        root.clipboard_clear()
        root.clipboard_append(copied_text)

def search_and_download():
    selected_titles = []
    for category, listbox_widget in listbox_widgets.items():
        selected_indices = listbox_widget.curselection()
        for index in selected_indices:
            selected_titles.append((category, listbox_widget.get(index)))
    
    if not selected_titles:
        messagebox.showinfo("Info", "No titles selected for download.")
        return

    for category, title in selected_titles:
        try:
            modified_title = title
            if category == "tv_shows":
                modified_title += " s01"
            elif category == "anime":
                modified_title += " dual audio"
            elif category == "movies":
                modified_title += " 1080p"
            
            command = ["python", "-m", "1337x", "-s", "SEEDERS", f'"{modified_title}"']
            subprocess.run(["powershell", "-c", " ".join(command)], check=True)
        except subprocess.CalledProcessError:
            messagebox.showwarning("Warning", f"Failed to download: {title}")

    marked_items.clear()

def view_wishlist():
    view_window = tk.Toplevel(root)
    view_window.title("View Wishlist")
    view_window.configure(background="black")
    view_window.geometry("1000x600")

    frame_width = 235  # Adjust width for each category frame

    for index, category in enumerate(categories):
        category_frame = tk.Frame(view_window, bg="black", width=frame_width)
        category_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        category_label = tk.Label(category_frame, text=category.capitalize(), font=("Helvetica", 16, "bold"), fg="red", bg="black")
        category_label.pack()

        category_list = tk.Listbox(category_frame, height=20, width=30, bg="white", fg="black", selectmode=tk.MULTIPLE)
        category_list.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(category_frame, orient=tk.VERTICAL, command=category_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        category_list.config(yscrollcommand=scrollbar.set)

        category_list.bind("<Button-1>", lambda event, lb=category_list: mark_item(event, lb))
        listbox_widgets[category] = category_list
        refresh_items_list(category, category_list)

        remove_all_button = tk.Button(category_frame, text="Remove All", 
                                      command=lambda cat=category, lb=category_list: delete_listings(cat),
                                      font=("Helvetica", 10), fg="red", bg="black")
        remove_all_button.pack(pady=5)

        remove_selected_button = tk.Button(category_frame, text="Remove Selected", 
                                           command=lambda cat=category, lb=category_list: delete_selected_items(cat, lb),
                                           font=("Helvetica", 10), fg="red", bg="black")
        remove_selected_button.pack(pady=5)

    download_button = tk.Button(view_window, text="Search & Download", command=search_and_download,
                                font=("Helvetica", 12, "bold"), fg="blue", bg="black")
    download_button.pack(pady=10)

    for lb in listbox_widgets.values():
        lb.bind("<Button-3>", lambda event, widget=lb: show_context_menu(event, widget))
        lb.bind("<Return>", lambda event: search_and_download())

def paste_items(entry_widget):
    try:
        pasted_text = root.clipboard_get()
        entry_widget.insert(tk.END, pasted_text)
    except tk.TclError:
        messagebox.showerror("Error", "Clipboard is empty!")

def create_context_menu(entry_widget):
    context_menu = tk.Menu(root, tearoff=0)
    context_menu.add_command(label="Paste", command=lambda: paste_items(entry_widget))
    entry_widget.bind("<Button-3>", lambda event: context_menu.tk_popup(event.x_root, event.y_root))

# ----------------------------------------
# Main GUI window setup
# ----------------------------------------
root = tk.Tk()
root.title("Michael Fedro's Wishlist Manager")
root.configure(background="black")

entry_widgets = {}
add_buttons = {}

for i, category in enumerate(categories):
    label = tk.Label(root, text=f"{category.capitalize()}:", font=("Helvetica", 12, "bold"), fg="red", bg="black")
    label.grid(row=i, column=0, padx=5, pady=5, sticky="w")

    entry_widget = tk.Text(root, height=5, width=30)
    entry_widget.grid(row=i, column=1, padx=5, pady=5)
    entry_widgets[category] = entry_widget
    create_context_menu(entry_widget)

    add_button = tk.Button(root, text=f"Add {category.capitalize()}", width=15, 
                           command=lambda cat=category, entry=entry_widget: add_item(cat, entry))
    add_button.grid(row=i, column=2, padx=5, pady=5, sticky="w")
    add_buttons[category] = add_button

view_button = tk.Button(root, text="See Wishlist", command=view_wishlist,
                        font=("Helvetica", 12, "bold"), fg="red", bg="black")
view_button.grid(row=len(categories), column=0, columnspan=3, pady=10, sticky="we")

# ----------------------------------------
# Start the GUI event loop
# ----------------------------------------
root.mainloop()
conn.close()
