import tkinter as tk
from tkinter import ttk
import psutil
import threading

class ProcessManagerApp:
    def __init__(self, master):
        self.master = master
        master.title("Task Manager")

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.label = ttk.Label(master, text="Search process:")
        self.label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.entry = ttk.Entry(master)
        self.entry.grid(row=0, column=1, padx=10, pady=5)

        self.search_button = ttk.Button(master, text="Search", command=self.search_process)
        self.search_button.grid(row=0, column=2, padx=10, pady=5)

        self.refresh_button = ttk.Button(master, text="Refresh", command=self.refresh_process_list)
        self.refresh_button.grid(row=0, column=3, padx=10, pady=5)

        self.memory_button = ttk.Button(master, text="Memory", command=self.sort_by_memory)
        self.memory_button.grid(row=0, column=4, padx=10, pady=5)

        self.cpu_button = ttk.Button(master, text="CPU", command=self.sort_by_cpu)
        self.cpu_button.grid(row=0, column=5, padx=10, pady=5)

        self.cpu_label = ttk.Label(master, text="CPU Usage: -")
        self.cpu_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.memory_label = ttk.Label(master, text="Memory Usage: -")
        self.memory_label.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        self.process_tree = ttk.Treeview(master, columns=("PID", "Name", "CPU%", "Memory%"), show="headings")
        self.process_tree.heading("PID", text="PID")
        self.process_tree.heading("Name", text="Name")
        self.process_tree.heading("CPU%", text="CPU%")
        self.process_tree.heading("Memory%", text="Memory%")
        self.process_tree.column("PID", width=80)
        self.process_tree.column("Name", width=200)
        self.process_tree.column("CPU%", width=100)
        self.process_tree.column("Memory%", width=100)
        self.process_tree.grid(row=3, column=0, columnspan=6, padx=10, pady=5, sticky="nsew")

        self.kill_button = ttk.Button(master, text="Kill", command=self.kill_process)
        self.kill_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        self.process_tree.bind("<Double-1>", self.populate_kill_button)
        self.populate_kill_button()

        self.update_process_list_thread()
        self.update_system_info_thread()

        self.style.configure("Custom.TButton", background="#4CAF50", foreground="white", font=("Arial", 10, "bold"))
        self.style.map("Custom.TButton", background=[('active', '#45a049')])

        self.style.configure("Treeview", background="#f0f0f0", foreground="black", fieldbackground="#d3d3d3", font=("Arial", 10))
        self.style.map("Treeview", background=[('selected', '#347083')])

    def update_process_list_thread(self):
        threading.Thread(target=self.update_process_list).start()

    def update_process_list(self):
        processes = psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent'])
        process_data = []
        for proc in processes:
            process_data.append((proc.info['pid'], proc.info['name'], f"{proc.info['cpu_percent']:.2f}%", f"{proc.info['memory_percent']:.2f}%"))
        self.master.after(0, self.update_process_tree, process_data)

    def update_process_tree(self, process_data):
        self.process_tree.delete(*self.process_tree.get_children())
        for data in process_data:
            self.process_tree.insert("", "end", values=data)

    def refresh_process_list(self):
        self.update_process_list_thread()

    def search_process(self):
        threading.Thread(target=self.search_process_thread).start()

    def search_process_thread(self):
        search_query = self.entry.get().lower()
        if search_query:
            processes = psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent'])
            matching_processes = [proc for proc in processes if search_query in proc.info['name'].lower()]
            process_data = [(proc.info['pid'], proc.info['name'], f"{proc.info['cpu_percent']:.2f}%", f"{proc.info['memory_percent']:.2f}%") for proc in matching_processes]
            self.master.after(0, self.update_process_tree, process_data)
        else:
            self.refresh_process_list()

    def kill_process(self):
        threading.Thread(target=self.kill_process_thread).start()

    def kill_process_thread(self):
        selected_item = self.process_tree.selection()
        if selected_item:
            selected_pid = self.process_tree.item(selected_item)['values'][0]
            selected_process = psutil.Process(selected_pid)
            try:
                selected_process.terminate()
            except psutil.AccessDenied:
                tk.messagebox.showerror("Access Denied", "Permission to terminate the selected process is denied.")
            except psutil.NoSuchProcess:
                tk.messagebox.showerror("Process Not Found", "The selected process is no longer running.")
            self.update_process_list_thread()

    def sort_by_memory(self):
        threading.Thread(target=self.sort_by_memory_thread).start()

    def sort_by_memory_thread(self):
        processes = psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent'])
        sorted_processes = sorted(processes, key=lambda proc: proc.info['memory_percent'], reverse=True)
        process_data = [(proc.info['pid'], proc.info['name'], f"{proc.info['cpu_percent']:.2f}%", f"{proc.info['memory_percent']:.2f}%") for proc in sorted_processes]
        self.master.after(0, self.update_process_tree, process_data)

    def sort_by_cpu(self):
        threading.Thread(target=self.sort_by_cpu_thread).start()

    def sort_by_cpu_thread(self):
        processes = psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent'])
        sorted_processes = sorted(processes, key=lambda proc: proc.info['cpu_percent'], reverse=True)
        process_data = [(proc.info['pid'], proc.info['name'], f"{proc.info['cpu_percent']:.2f}%", f"{proc.info['memory_percent']:.2f}%") for proc in sorted_processes]
        self.master.after(0, self.update_process_tree, process_data)

    def update_system_info_thread(self):
        threading.Thread(target=self.update_system_info).start()

    def update_system_info(self):
        while True:
            cpu_percent = psutil.cpu_percent(interval=0.5)  # Reduce interval for more accurate CPU usage readings
            memory_percent = psutil.virtual_memory().percent
            self.cpu_label.config(text=f"CPU Usage: {cpu_percent}%")
            self.memory_label.config(text=f"Memory Usage: {memory_percent}%")
            self.master.after(1000)

    def populate_kill_button(self, event=None):
        selected_item = self.process_tree.selection()
        if selected_item:
            self.kill_button.config(state="normal")
        else:
            self.kill_button.config(state="disabled")

def main():
    root = tk.Tk()
    app = ProcessManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
