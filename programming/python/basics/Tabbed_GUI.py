#  Tabbed GUI
# Step 1: Import the Tkinter Library
import tkinter as tk
from tkinter import ttk

# Step 2: Create a Main Window
window = tk.Tk()
window.title("Tabbed GUI")

# Step 3: Create a Notebook Widget
notebook = ttk.Notebook(window)

# Step 4: Create Frames for Tabs
tab1 = tk.Frame(notebook)
tab2 = tk.Frame(notebook)

# Step 5: Add Frames to the Notebook
notebook.add(tab1, text="Tab 1")
notebook.add(tab2, text="Tab 2")

# Step 6: Pack the Notebook
notebook.pack(expand=True, fill="both")

# Step 7: Create Labels for Tab 1
label_tab1 = tk.Label(tab1, text="Hello! This is Tab 1", width=50, height=25)
label_tab1.pack()

# Step 8: Create Labels for Tab 2
label_tab2 = tk.Label(tab2, text="Goodbye! This is Tab 2", width=50, height=25)
label_tab2.pack()

# Step 9: Configure Notebook Packing for Layout
notebook.pack(expand=True, fill="both")

# Step 10: Test the Program
window.mainloop()