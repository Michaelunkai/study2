import psutil
import tkinter as tk
from tkinter import ttk

class SystemMonitor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("System Monitoring Dashboard")
        self.geometry("600x700")

        self.configure(bg="#fff0e0")  # Cream white background color

        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Lobster", 12, "bold"), background="#fff0e0")  # Lobster font, bold, cream white background
        self.style.configure("TLabelFrame", font=("Lobster", 14, "bold"), background="#fff0e0")  # Lobster font, bold, cream white background
        self.style.configure("TProgressbar", background="#f0e0d0")  # Progress bar background color

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(expand=True, padx=20, pady=20)

        # Memory Usage (%)
        self.memory_frame = ttk.LabelFrame(self.main_frame, text="Memory Usage")
        self.memory_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.memory_percent_label = ttk.Label(self.memory_frame, text="")
        self.memory_percent_label.pack(padx=5, pady=5)

        self.memory_progress = ttk.Progressbar(self.memory_frame, orient="horizontal", length=400, mode="determinate")
        self.memory_progress.pack(padx=5, pady=5)

        # Memory Usage (MB)
        self.memory_mb_label = ttk.Label(self.memory_frame, text="")
        self.memory_mb_label.pack(padx=5, pady=5)

        # Top Memory-consuming Processes
        self.memory_processes_label = ttk.Label(self.main_frame, text="Top 20 Memory-consuming Processes:")
        self.memory_processes_label.pack(padx=10, pady=10, anchor=tk.W)

        self.memory_processes_info_label = ttk.Label(self.main_frame, wraplength=780)
        self.memory_processes_info_label.pack(padx=10, pady=10, anchor=tk.W)

        self.update_system_info()

    def update_system_info(self):
        # Memory Usage (%)
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        self.memory_percent_label.config(text="{:.2f}%".format(memory_percent))
        self.memory_progress["value"] = memory_percent

        # Memory Usage (MB)
        memory_usage_mb = memory.used / (1024 ** 2)  # Convert bytes to megabytes
        memory_total_mb = memory.total / (1024 ** 2)  # Convert bytes to megabytes
        self.memory_mb_label.config(text="{:.2f} MB / {:.2f} MB".format(memory_usage_mb, memory_total_mb))

        # Top Memory-consuming Processes
        memory_processes_info = self.get_top_processes()
        self.memory_processes_info_label["text"] = memory_processes_info

        self.after(500, self.update_system_info)  # Update every 0.5 seconds

    def get_top_processes(self):
        processes = sorted(psutil.process_iter(attrs=['pid', 'name', 'memory_info']), key=lambda x: x.info['memory_info'].rss, reverse=True)[:20]
        info = "PID  Name           Memory Usage (%)  Memory Usage (MB)\n"
        for process in processes:
            memory_usage_percent = (process.info['memory_info'].rss / psutil.virtual_memory().total) * 100
            memory_usage_mb = process.info['memory_info'].rss / (1024 ** 2)  # Convert bytes to megabytes
            info += "{:<5} {:<15} {:.2f}%           {:.2f} MB\n".format(process.info['pid'], process.info['name'], memory_usage_percent, memory_usage_mb)
        return info

if __name__ == "__main__":
    app = SystemMonitor()
    app.mainloop()
