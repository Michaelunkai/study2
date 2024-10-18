import tkinter as tk

class TaskWindow:
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(root, title="New Window")
        self.listbox = tk.Listbox(self.window, selectmode=tk.SINGLE)
        self.listbox.pack(pady=10)
        self.entry = tk.Entry(self.window)
        self.entry.pack(pady=10)
        self.add_button = tk.Button(self.window, text="Add", command=self.add_task)
        self.remove_button = tk.Button(self.window, text="Remove", command=self.remove_task)
        self.change_button = tk.Button(self.window, text="Change", command=self.change_task)
        for button in [self.add_button, self.remove_button, self.change_button]:
            button.pack(side=tk.LEFT, padx=5)

    def add_task(self):
        task = self.entry.get()
        if task:
            self.listbox.insert(tk.END, task)
            self.entry.delete(0, tk.END)
            save_tasks()

    def remove_task(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            self.listbox.delete(selected_index)
            save_tasks()

    def change_task(self):
        selected_index = self.listbox.curselection()
        new_task = self.entry.get()
        if selected_index and new_task:
            self.listbox.delete(selected_index)
            self.listbox.insert(selected_index, new_task)
            self.entry.delete(0, tk.END)
            save_tasks()

def add_task():
    task = entry.get()
    if task:
        listbox.insert(tk.END, task)
        entry.delete(0, tk.END)
        save_tasks()

def remove_task():
    selected_index = listbox.curselection()
    if selected_index:
        listbox.delete(selected_index)
        save_tasks()

def change_task():
    selected_index = listbox.curselection()
    new_task = entry.get()
    if selected_index and new_task:
        listbox.delete(selected_index)
        listbox.insert(selected_index, new_task)
        entry.delete(0, tk.END)
        save_tasks()

def save_tasks():
    with open("tasks.txt", "w") as file:
        file.write("\n".join(listbox.get(0, tk.END)))

def load_tasks():
    try:
        with open("tasks.txt", "r") as file:
            listbox.insert(tk.END, *file.read().splitlines())
    except FileNotFoundError:
        pass

app = tk.Tk()
app.title("To-Do App")

listbox = tk.Listbox(app, selectmode=tk.SINGLE)
listbox.pack(pady=10)

entry = tk.Entry(app)
entry.pack(pady=10)

buttons = [
    tk.Button(app, text="Add", command=add_task),
    tk.Button(app, text="Remove", command=remove_task),
    tk.Button(app, text="Change", command=change_task),
]

for button in buttons:
    button.pack(side=tk.LEFT, padx=5)

load_tasks()
app.windows = []
app.mainloop()