import os
import sys
import shutil
import sqlite3
import tempfile
import subprocess
import paramiko
import tkinter as tk
from tkinter import ttk, messagebox

# -------------------------------
# Configuration and file settings
# -------------------------------
HOSTNAME = "54.173.176.93"
USERNAME = "ubuntu"
KEY_PATH = r"C:\backup\windowsapps\Credentials\AWS\key.pem"
REMOTE_DB_PATH = "/home/ubuntu/wishlist/wishlist.db"
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
        local_temp_path = os.path.join(tempfile.gettempdir(), "wishlist_remote.db")
        sftp.get(REMOTE_DB_PATH, local_temp_path)
        sftp.close()
        ssh.close()

        shutil.copy(local_temp_path, LOCAL_DB_FILENAME)
        return LOCAL_DB_FILENAME
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download remote database: {e}")
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
        messagebox.showerror("Error", f"Failed to upload database: {e}")


# ----------------------------------------
# Database initialization
# ----------------------------------------

def init_local_db():
    """Initialize the local SQLite database, downloading it if missing."""
    if not os.path.exists(LOCAL_DB_FILENAME):
        download_remote_db()

    conn = sqlite3.connect(LOCAL_DB_FILENAME)
    cursor = conn.cursor()

    tables = {
        "movies": "CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY, title TEXT)",
        "tv_shows": "CREATE TABLE IF NOT EXISTS tv_shows (id INTEGER PRIMARY KEY, title TEXT)",
        "games": "CREATE TABLE IF NOT EXISTS games (id INTEGER PRIMARY KEY, title TEXT)",
        "anime": "CREATE TABLE IF NOT EXISTS anime (id INTEGER PRIMARY KEY, title TEXT)",
    }
    for create_sql in tables.values():
        cursor.execute(create_sql)
    conn.commit()
    return conn, cursor


# Initialize DB
conn, cursor = init_local_db()

# ----------------------------------------
# Application data structures
# ----------------------------------------

actions_by_category = {
    "movies": lambda title: f"{title} 1080p",
    "tv_shows": lambda title: f"{title} s01",
    "anime": lambda title: f"{title} dual audio",
    "games": lambda title: title,
}

categories = list(actions_by_category.keys())
items_ids = {category: [] for category in categories}
listbox_widgets: dict[str, tk.Listbox] = {}
marked_items: set[tuple[str, int]] = set()  # (category, index)

# ----------------------------------------
# Helper functions
# ----------------------------------------

def refresh_items_list(category: str):
    """Refresh the listbox with DB items for a given category."""
    lb = listbox_widgets[category]
    lb.delete(0, tk.END)
    items_ids[category].clear()
    cursor.execute(f"SELECT id, title FROM {category}")
    for item_id, title in cursor.fetchall():
        lb.insert(tk.END, title)
        items_ids[category].append(item_id)


def perform_download(category: str, title: str):
    """Run a PowerShell 1337x search/download for a single title."""
    try:
        modified_title = actions_by_category[category](title)
        command = [
            "powershell",
            "-c",
            f"python -m 1337x -s SEEDERS \"{modified_title}\"",
        ]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        messagebox.showwarning("Warning", f"Failed to download: {title}")


# ----------------------------------------
# CRUD operations
# ----------------------------------------

def add_item(category: str, entry_widget: tk.Text):
    titles = [t.strip() for t in entry_widget.get("1.0", "end-1c").split("\n") if t.strip()]
    if not titles:
        return
    cursor.executemany(
        f"INSERT INTO {category} (title) VALUES (?)", [(title,) for title in titles]
    )
    conn.commit()
    upload_remote_db()
    refresh_items_list(category)
    messagebox.showinfo("Success", f"Added {len(titles)} {category.replace('_', ' ').title()} item(s)")
    entry_widget.delete("1.0", tk.END)


def delete_listings(category: str):
    if not messagebox.askyesno(
        "Confirm", f"Delete ALL {category.replace('_', ' ')} items?"):
        return
    cursor.execute(f"DELETE FROM {category}")
    conn.commit()
    upload_remote_db()
    refresh_items_list(category)


def delete_selected_items(category: str):
    lb = listbox_widgets[category]
    indices = lb.curselection()
    if not indices:
        messagebox.showerror("Error", "No items selected")
        return
    if not messagebox.askyesno("Confirm", "Delete selected item(s)?"):
        return
    for idx in reversed(indices):
        item_id = items_ids[category][idx]
        cursor.execute(f"DELETE FROM {category} WHERE id=?", (item_id,))
    conn.commit()
    upload_remote_db()
    refresh_items_list(category)


# ----------------------------------------
# Download helpers
# ----------------------------------------

def download_selected():
    selections: list[tuple[str, str]] = []
    for category, lb in listbox_widgets.items():
        for idx in lb.curselection():
            selections.append((category, lb.get(idx)))
    if not selections:
        messagebox.showinfo("Info", "Nothing selected to download")
        return
    for category, title in selections:
        perform_download(category, title)


def run_all(category: str):
    lb = listbox_widgets[category]
    titles = lb.get(0, tk.END)
    if not titles:
        messagebox.showinfo("Info", f"No {category} to run")
        return
    if not messagebox.askyesno(
        "Run All", f"Run ALL {len(titles)} {category} items one after another?"):
        return
    for title in titles:
        perform_download(category, title)


# ----------------------------------------
# UI helpers
# ----------------------------------------

def style_ttk():
    style = ttk.Style()
    if sys.platform == "win32":
        style.theme_use("vista")
    else:
        style.theme_use("clam")
    style.configure("TFrame", background="#121212")
    style.configure("TLabel", background="#121212", foreground="#e53935", font=("Helvetica", 12, "bold"))
    style.configure("TButton", font=("Helvetica", 10, "bold"), padding=6)
    style.map("TButton", foreground=[("active", "#ffffff")])


# ----------------------------------------
# Context menu for paste
# ----------------------------------------

def create_context_menu(widget: tk.Text):
    menu = tk.Menu(widget, tearoff=0)
    menu.add_command(label="Paste", command=lambda: widget.event_generate("<<Paste>>"))
    widget.bind("<Button-3>", lambda e: menu.tk_popup(e.x_root, e.y_root))


# ----------------------------------------
# Build main window
# ----------------------------------------

root = tk.Tk()
root.title("Michael Fedro's Wishlist Manager")
root.geometry("820x560")
root.configure(bg="#121212")
root.minsize(820, 560)
style_ttk()

entry_widgets: dict[str, tk.Text] = {}

for row, category in enumerate(categories):
    ttk.Label(root, text=f"{category.capitalize()}:").grid(row=row, column=0, sticky="w", padx=10, pady=6)
    text = tk.Text(root, height=4, width=35, bg="#1e1e1e", fg="#ffffff", insertbackground="#ffffff")
    text.grid(row=row, column=1, padx=5, pady=5, sticky="we")
    create_context_menu(text)
    entry_widgets[category] = text

    ttk.Button(
        root,
        text=f"Add {category.capitalize()}",
        command=lambda c=category: add_item(c, entry_widgets[c]),
    ).grid(row=row, column=2, padx=5, pady=5)

root.grid_columnconfigure(1, weight=1)


# ----------------------------------------
# Wishlist viewer
# ----------------------------------------

def view_wishlist():
    viewer = tk.Toplevel(root)
    viewer.title("Wishlist")
    viewer.configure(bg="#121212")
    viewer.geometry("1000x620")

    container = ttk.Frame(viewer)
    container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    for col, category in enumerate(categories):
        frame = ttk.Frame(container)
        frame.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")
        container.grid_columnconfigure(col, weight=1)
        ttk.Label(frame, text=category.capitalize()).pack(anchor="n", pady=(0, 4))

        lb = tk.Listbox(
            frame,
            selectmode=tk.MULTIPLE,
            bg="#1e1e1e",
            fg="#dcdcdc",
            relief=tk.FLAT,
            highlightthickness=0,
        )
        lb.pack(fill=tk.BOTH, expand=True)
        listbox_widgets[category] = lb
        refresh_items_list(category)

        # Scrollbar
        sb = ttk.Scrollbar(frame, orient="vertical", command=lb.yview)
        sb.place(relx=1, rely=0, relheight=1, anchor="ne")
        lb.configure(yscrollcommand=sb.set)

        # Action buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=4)
        ttk.Button(
            btn_frame,
            text="Remove All",
            command=lambda c=category: delete_listings(c),
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            btn_frame,
            text="Remove Selected",
            command=lambda c=category: delete_selected_items(c),
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            btn_frame,
            text="Run All",
            command=lambda c=category: run_all(c),
        ).pack(side=tk.LEFT, padx=2)

    # Bottom download selected button
    ttk.Button(
        viewer,
        text="Search & Download Selected",
        command=download_selected,
    ).pack(pady=10)


# ----------------------------------------
# Main controls
# ----------------------------------------

ttk.Button(
    root,
    text="See Wishlist",
    command=view_wishlist,
).grid(row=len(categories), column=0, columnspan=3, pady=15)

# ----------------------------------------
# Start loop
# ----------------------------------------
root.mainloop()
conn.close()
