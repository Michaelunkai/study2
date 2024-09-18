# Step 1: Import the Tkinter Library
import tkinter as tk

# Step 2: Define Functions

# Function to create a simple new window
def create_window():
    new_window = tk.Toplevel(main_window)
    # Additional functionality and customization can be added here
    main_window.destroy()  # Close the main window

# Complex version with additional features and customization
def create_complex_window():
    complex_window = tk.Toplevel(main_window)
    complex_window.title("Complex Window")
    
    label = tk.Label(complex_window, text="This is a complex window!")
    label.pack(pady=10)
    
    close_button = tk.Button(complex_window, text="Close", command=complex_window.destroy)
    close_button.pack(pady=10)
    
    main_window.destroy()

# Step 3: Create a Main Window
main_window = tk.Tk()

# step 4 : Create Buttons to generate windows
new_window_button = tk.Button(main_window, text="Create New Window", command=create_window)
new_window_button.pack()

complex_window_button = tk.Button(main_window, text="Create Complex Window", command=create_complex_window)
complex_window_button.pack()

# Step 5: Test the Program
main_window.mainloop()