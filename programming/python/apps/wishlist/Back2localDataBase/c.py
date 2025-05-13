import os
import sys
import shutil
import sqlite3
import tempfile
import subprocess
import paramiko
import tkinter as tk
from tkinter import ttk, messagebox

"""
Michael Fedro's single‑window Wishlist Manager
------------------------------------------------
* One dark‑theme GUI containing **both** the entry section and the live wishlist view.
* Per‑category controls: **Add**, **Run All**, **Remove All**, **Remove Selected**.
* Global **Search & Download Selected** button.
* SSH/Paramiko sync preserved.
"""
# -------------------------------
# Configuration
# -------------------------------
HOSTNAME = "54.173.176.93"
USERNAME = "ubuntu"
KEY_PATH = r"C:\backup\windowsapps\Credentials\AWS\key.pem"
REMOTE_DB_PATH = "/home/ubuntu/wishlist/wishlist.db"
LOCAL_DB_FILENAME = "wishlist.db"

# ----------------------------------------
# Remote sync via Paramiko/SFTP
# ----------------------------------------

def download_remote_db():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=HOSTNAME, username=USERNAME, key_filename=KEY_PATH)
        sftp = ssh.open_sftp()
        temp_path = os.path.join(tempfile.gettempdir(), "wishlist_remote.db")
        sftp.get(REMOTE_DB_PATH, temp_path)
        sftp.close(); ssh.close()
        shutil.copy(temp_path, LOCAL_DB_FILENAME)
    except Exception as exc:
        messagebox.showerror("Error", f"Download failed: {exc}")
        sys.exit(1)

def upload_remote_db():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=HOSTNAME, username=USERNAME, key_filename=KEY_PATH)
        sftp = ssh.open_sftp()
        sftp.put(LOCAL_DB_FILENAME, REMOTE_DB_PATH)
        sftp.close(); ssh.close()
    except Exception as exc:
        messagebox.showerror("Error", f"Upload failed: {exc}")

# ----------------------------------------
# SQLite initialisation
# ----------------------------------------

def init_db():
    if not os.path.exists(LOCAL_DB_FILENAME):
        download_remote_db()
    connection = sqlite3.connect(LOCAL_DB_FILENAME)
    cur = connection.cursor()
    for table in ("movies", "tv_shows", "games", "anime"):
        cur.execute(f"CREATE TABLE IF NOT EXISTS {table} (id INTEGER PRIMARY KEY, title TEXT)")
    connection.commit()
    return connection, cur

conn, cursor = init_db()

# ----------------------------------------
# App‑wide structures
# ----------------------------------------

categories = ["movies", "tv_shows", "games", "anime"]
items_ids: dict[str, list[int]] = {c: [] for c in categories}
entry_widgets: dict[str, tk.Text] = {}
listbox_widgets: dict[str, tk.Listbox] = {}

modify_title = {
    "movies": lambda t: f"{t} 1080p",
    "tv_shows": lambda t: f"{t} s01",
    "anime": lambda t: f"{t} dual audio",
    "games": lambda t: t,
}

# ----------------------------------------
# DB helpers
# ----------------------------------------

def refresh_items(category: str):
    lb = listbox_widgets[category]
    lb.delete(0, tk.END)
    items_ids[category].clear()
    cursor.execute(f"SELECT id, title FROM {category}")
    for item_id, title in cursor.fetchall():
        lb.insert(tk.END, title)
        items_ids[category].append(item_id)

# ----------------------------------------
# Core actions
# ----------------------------------------

def add_item(category: str):
    text_widget = entry_widgets[category]
    titles = [t.strip() for t in text_widget.get("1.0", "end-1c").split("\n") if t.strip()]
    if not titles:
        return
    cursor.executemany(f"INSERT INTO {category} (title) VALUES (?)", [(t,) for t in titles])
    conn.commit(); upload_remote_db(); refresh_items(category)
    text_widget.delete("1.0", tk.END)


def delete_all(category: str):
    if not messagebox.askyesno("Confirm", f"Delete ALL {category.replace('_',' ')}?"):
        return
    cursor.execute(f"DELETE FROM {category}"); conn.commit(); upload_remote_db(); refresh_items(category)


def delete_selected(category: str):
    lb = listbox_widgets[category]
    sel = lb.curselection()
    if not sel:
        return
    if not messagebox.askyesno("Confirm", "Delete selected item(s)?"):
        return
    for idx in reversed(sel):
        cursor.execute(f"DELETE FROM {category} WHERE id=?", (items_ids[category][idx],))
    conn.commit(); upload_remote_db(); refresh_items(category)


def run_download(category: str, title: str):
    try:
        mod_title = modify_title[category](title)
        cmd = ["powershell", "-c", f"python -m 1337x -s SEEDERS \"{mod_title}\""]
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        messagebox.showwarning("Warning", f"Failed: {title}")


def run_all(category: str):
    lb = listbox_widgets[category]
    titles = lb.get(0, tk.END)
    if not titles:
        return
    if not messagebox.askyesno("Run All", f"Run ALL {len(titles)} {category}?"):
        return
    for t in titles:
        run_download(category, t)


def download_selected():
    collected: list[tuple[str, str]] = []
    for cat, lb in listbox_widgets.items():
        collected.extend([(cat, lb.get(i)) for i in lb.curselection()])
    if not collected:
        messagebox.showinfo("Info", "Nothing selected")
        return
    for cat, tit in collected:
        run_download(cat, tit)

# ----------------------------------------
# UI helpers
# ----------------------------------------

def paste_from_clip(event):
    try:
        content = root.clipboard_get()
        event.widget.insert(tk.END, content)
    except tk.TclError:
        pass


def ctx_menu(widget: tk.Text):
    m = tk.Menu(widget, tearoff=0)
    m.add_command(label="Paste", command=lambda w=widget: w.event_generate("<<Paste>>"))
    widget.bind("<Button-3>", lambda e, m=m: m.tk_popup(e.x_root, e.y_root))


def style_dark():
    st = ttk.Style()
    if sys.platform == "win32":
        st.theme_use("vista")
    else:
        st.theme_use("clam")
    bg = "#121212"; fg = "#e53935"; txt = "#dcdcdc"
    st.configure("TFrame", background=bg)
    st.configure("TLabel", background=bg, foreground=fg, font=("Helvetica", 12, "bold"))
    st.configure("TButton", font=("Helvetica", 10, "bold"))
    st.map("TButton", foreground=[("active", "#ffffff")])

# ----------------------------------------
# Build interface (single window)
# ----------------------------------------
root = tk.Tk()
root.title("Michael Fedro's Wishlist Manager")
root.geometry("1200x650")
root.configure(bg="#121212")
style_dark()

# --- Entry section at the top
entry_frame = ttk.Frame(root)
entry_frame.pack(fill=tk.X, padx=12, pady=8)

for col, cat in enumerate(categories):
    sub = ttk.Frame(entry_frame)
    sub.grid(row=0, column=col, padx=6, sticky="n")
    ttk.Label(sub, text=f"{cat.capitalize()}").pack(anchor="w")
    txt = tk.Text(sub, height=3, width=23, bg="#1e1e1e", fg="#ffffff", insertbackground="#ffffff")
    txt.pack()
    ctx_menu(txt)
    entry_widgets[cat] = txt
    ttk.Button(sub, text="Add", command=lambda c=cat: add_item(c)).pack(pady=2, fill=tk.X)

# --- Wishlist section below
list_container = ttk.Frame(root)
list_container.pack(fill=tk.BOTH, expand=True, padx=12, pady=4)

for col, cat in enumerate(categories):
    lst_frame = ttk.Frame(list_container)
    lst_frame.grid(row=0, column=col, padx=6, sticky="nsew")
    list_container.grid_columnconfigure(col, weight=1)
    ttk.Label(lst_frame, text=cat.capitalize()).pack(anchor="n")
    lb = tk.Listbox(lst_frame, selectmode=tk.MULTIPLE, bg="#1e1e1e", fg="white", relief=tk.FLAT, highlightthickness=0)
    lb.pack(fill=tk.BOTH, expand=True)
    listbox_widgets[cat] = lb
    refresh_items(cat)
    sb = ttk.Scrollbar(lst_frame, orient="vertical", command=lb.yview)
    sb.place(relx=1, rely=0, relheight=1, anchor="ne"); lb.config(yscrollcommand=sb.set)

    # action buttons
    btnf = ttk.Frame(lst_frame)
    btnf.pack(fill=tk.X, pady=2)
    for lbl, cmd in (
        ("Remove All", lambda c=cat: delete_all(c)),
        ("Remove Sel", lambda c=cat: delete_selected(c)),
        ("Run All", lambda c=cat: run_all(c)),
    ):
        ttk.Button(btnf, text=lbl, command=cmd).pack(side=tk.LEFT, padx=1)

# --- Global Download Selected button

ttk.Button(root, text="Search & Download Selected", command=download_selected).pack(pady=10)

root.mainloop()
conn.close()

