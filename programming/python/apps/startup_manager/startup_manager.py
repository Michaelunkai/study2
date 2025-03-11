import os
import subprocess
import csv
import io
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar
import tkinter.font as tkFont
import winreg
import winshell

# Paths
startup_folder = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup")

def is_critical(app_entry):
    """
    Determines if a startup entry is critical (i.e. shouldn't be disabled).
    For this example, any entry whose target path starts with r"C:\Windows" is flagged.
    """
    # For registry and scheduled items, the target path is after '->'
    if "[Registry]" in app_entry or "[Scheduled]" in app_entry:
        if "->" in app_entry:
            target = app_entry.split("->")[1].strip()
            if target.lower().startswith(r"c:\windows"):
                return True
    elif "[Folder]" in app_entry:
        # Try to read the target of the shortcut from the startup folder
        app_name = app_entry.replace("[Folder] ", "").strip()
        shortcut_path = os.path.join(startup_folder, app_name)
        try:
            with winshell.shortcut(shortcut_path) as link:
                target = link.path
                if target and target.lower().startswith(r"c:\windows"):
                    return True
        except Exception:
            pass
    return False

# Function to get startup applications from the Windows Registry
def get_registry_startup_apps():
    startup_apps = []
    for hive, key_path in [
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"),
    ]:
        try:
            with winreg.OpenKey(hive, key_path, 0, winreg.KEY_READ) as key:
                i = 0
                while True:
                    try:
                        name, value, _ = winreg.EnumValue(key, i)
                        startup_apps.append(f"[Registry] {name} -> {value}")
                        i += 1
                    except OSError:
                        break
        except FileNotFoundError:
            continue
    return startup_apps

# Function to get startup applications from the Startup Folder
def get_folder_startup_apps():
    return [f"[Folder] {app}" for app in os.listdir(startup_folder) if app.endswith(".lnk")]

# Function to get scheduled tasks that run at logon and are enabled
def get_scheduled_startup_apps():
    scheduled_apps = []
    try:
        output = subprocess.check_output("schtasks /Query /FO CSV /V", shell=True, text=True)
        reader = csv.DictReader(io.StringIO(output))
        for row in reader:
            schedule_type = row.get("Schedule Type", "").strip().lower()
            status = row.get("Status", "").strip().lower()
            if schedule_type == "at logon" and status != "disabled":
                task_name = row.get("TaskName", "").strip()
                task_to_run = row.get("Task To Run", "").strip()
                scheduled_apps.append(f"[Scheduled] {task_name} -> {task_to_run}")
    except Exception as e:
        print("Error retrieving scheduled tasks:", e)
    return scheduled_apps

# Function to refresh the startup list
def refresh_startup_list():
    startup_listbox.delete(0, tk.END)
    startup_apps = get_registry_startup_apps() + get_folder_startup_apps() + get_scheduled_startup_apps()
    for index, app in enumerate(startup_apps):
        startup_listbox.insert(tk.END, app)
        if is_critical(app):
            startup_listbox.itemconfig(index, fg="red")

# Function to add an application to startup (via the Startup Folder)
def add_to_startup():
    file_path = filedialog.askopenfilename(filetypes=[("Executable Files", "*.exe")])
    if not file_path:
        return
    app_name = os.path.basename(file_path)
    shortcut_path = os.path.join(startup_folder, app_name + ".lnk")
    try:
        with winshell.shortcut(shortcut_path) as link:
            link.path = file_path
            link.description = f"Startup shortcut for {app_name}"
        messagebox.showinfo("Success", f"{app_name} added to startup!")
        refresh_startup_list()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to remove an application from startup (only from Startup Folder or Registry)
def remove_from_startup():
    selected_item = startup_listbox.get(tk.ACTIVE)
    if not selected_item:
        return

    if is_critical(selected_item):
        messagebox.showwarning("Warning", "This startup item is critical and should not be disabled!")
        return

    if "[Folder]" in selected_item:
        app_name = selected_item.replace("[Folder] ", "").strip()
        shortcut_path = os.path.join(startup_folder, app_name)
        try:
            os.remove(shortcut_path)
            messagebox.showinfo("Success", f"{app_name} removed from startup folder!")
            refresh_startup_list()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    elif "[Registry]" in selected_item:
        app_name = selected_item.split(" -> ")[0].replace("[Registry] ", "").strip()
        for hive, key_path in [
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"),
        ]:
            try:
                with winreg.OpenKey(hive, key_path, 0, winreg.KEY_SET_VALUE) as key:
                    winreg.DeleteValue(key, app_name)
                    messagebox.showinfo("Success", f"{app_name} removed from registry startup!")
                    refresh_startup_list()
                    return
            except (FileNotFoundError, OSError):
                continue
        messagebox.showerror("Error", f"Failed to remove {app_name} from registry.")
    else:
        messagebox.showwarning("Warning", "Removal of scheduled tasks is not supported via this interface.")

# GUI setup
root = tk.Tk()
root.title("Windows Startup Manager")
root.geometry("750x550")
root.configure(bg="#f0f0f0")  # Light gray background

# Set a bulky, bold font for UI elements
bold_font = tkFont.Font(family="Helvetica", size=12, weight="bold")
title_font = tkFont.Font(family="Helvetica", size=16, weight="bold")

# Title label
title_label = tk.Label(root, text="Windows Startup Manager", font=title_font, bg="#f0f0f0")
title_label.pack(pady=10)

frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=10)

add_button = tk.Button(frame, text="Add Application to Startup", command=add_to_startup, font=bold_font, bg="#ffffff", relief="groove", padx=10, pady=5)
add_button.pack(pady=5, side=tk.LEFT, padx=10)

remove_button = tk.Button(frame, text="Remove Selected from Startup", command=remove_from_startup, font=bold_font, bg="#ffffff", relief="groove", padx=10, pady=5)
remove_button.pack(pady=5, side=tk.LEFT, padx=10)

scrollbar = Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0,10))

startup_listbox = Listbox(root, yscrollcommand=scrollbar.set, width=100, height=20, font=bold_font, bg="#ffffff", relief="sunken")
startup_listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
scrollbar.config(command=startup_listbox.yview)

refresh_startup_list()

root.mainloop()
