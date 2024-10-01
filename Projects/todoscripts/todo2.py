import tkinter as tk
from tkinter import messagebox

# Define the add_task function to add tasks to the list
def add_task():
    task_name = task_entry.get()
    if task_name:
        tasks.append({"name": task_name, "completed": False})
        update_task_list()
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Please enter a task.")

# Define the mark_completed function to mark a task as completed
def mark_completed():
    selected_task = task_listbox.curselection()
    if selected_task:
        index = selected_task[0]
        tasks[index]["completed"] = True
        # Check if the task is completed and remove it from the list
        if tasks[index]["completed"]:
            del tasks[index]
        update_task_list()
    else:
        messagebox.showwarning("Warning", "Please select a task to mark as completed.")

# Define a function to update the task list
def update_task_list():
    task_listbox.delete(0, tk.END)
    for task in tasks:
        status = "Completed" if task["completed"] else "Not Completed"
        task_listbox.insert(tk.END, f"{task['name']} - {status}")

# Create the main window
app = tk.Tk()
app.title("To-Do App")

# Create a text entry field and add task button
task_entry = tk.Entry(app, width=30)
task_entry.grid(row=0, column=0, padx=10, pady=10)

add_button = tk.Button(app, text="Add Task", width=10, command=add_task)
add_button.grid(row=0, column=1, padx=10, pady=10)

# Create a task listbox
task_listbox = tk.Listbox(app, width=40, height=10)
task_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Create a mark as completed button
mark_button = tk.Button(app, text="Mark as Completed", width=15, command=mark_completed)
mark_button.grid(row=2, column=0, padx=10, pady=10)

# Define an initial list of tasks
tasks = []

# Start the Tkinter main loop
app.mainloop()