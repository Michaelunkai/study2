import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import sys
import os

class OneLinerLab(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("One-Liner Command Lab")
        self.geometry("1024x768")
        self.configure(bg="#f0f0f0")
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background="#f0f0f0", borderwidth=0)
        style.configure("TNotebook.Tab", background="#e0e0e0", padding=[20, 10], font=('Arial', 12))
        style.map("TNotebook.Tab", background=[("selected", "#ffffff")])
        
        style.configure("TFrame", background="#ffffff")
        style.configure("TLabel", background="#ffffff", font=('Arial', 14))
        style.configure("TButton", font=('Arial', 12), padding=10)
        style.configure("TEntry", font=('Courier', 12))

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.lab1 = ttk.Frame(self.notebook)
        self.lab2 = ttk.Frame(self.notebook)

        self.notebook.add(self.lab1, text="Lab 1")
        self.notebook.add(self.lab2, text="Lab 2")

        self.create_lab1()
        self.create_lab2()

        self.finish_button = ttk.Button(self, text="Finish", command=self.finish, style="TButton")
        self.finish_button.pack(pady=20)

    def create_lab1(self):
        tasks = [
            "Task 1: List all files, count them, and display disk usage",
            "Task 2: Find all Python files, count lines, and create a backup",
            "Task 3: Update system, install Python packages, and run a test script",
            "Task 4: Create a directory structure, generate random files, and compress",
            "Task 5: Clone a Git repo, install dependencies, and run tests"
        ]

        commands = [
            'ls -R | wc -l && du -sh . && echo "Total files and disk usage displayed" && date',
            'find . -name "*.py" | xargs wc -l && mkdir -p backup && cp *.py backup/ && echo "Python files processed and backed up" && ls -R backup',
            'sudo apt update && sudo apt upgrade -y && pip install requests beautifulsoup4 && python -c "import requests, beautifulsoup4; print(\'Packages installed\')" && python test_script.py',
            'mkdir -p project/{src,tests,docs} && for i in {1..5}; do dd if=/dev/urandom of=project/file$i.bin bs=1M count=1; done && tar -czvf project.tar.gz project && echo "Project structure created and compressed"',
            'git clone https://github.com/example/repo.git && cd repo && pip install -r requirements.txt && python -m pytest tests/ && echo "Repository cloned, dependencies installed, and tests run"'
        ]

        self.create_lab_content(self.lab1, tasks, commands)

    def create_lab2(self):
        tasks = [
            "Task 1: Scan network, save results, and analyze open ports",
            "Task 2: Download website, extract links, and check their status",
            "Task 3: Convert images to grayscale, resize, and create a collage",
            "Task 4: Generate random data, analyze it, and create visualizations",
            "Task 5: Perform system maintenance, create a report, and send via email"
        ]

        commands = [
            'nmap -sn 192.168.1.0/24 > network_scan.txt && cat network_scan.txt | grep "Nmap scan report" | wc -l && nmap -p- -iL network_scan.txt -oN open_ports.txt && echo "Network scanned and open ports analyzed"',
            'wget -r -l 1 -p https://example.com && grep -roP "(?<=href=\")https?://[^\"]*" example.com | sort -u > links.txt && cat links.txt | xargs -n1 -P10 curl -o /dev/null --silent --head --write-out "%{url_effective} %{http_code}\\n" > status.txt && cat status.txt | sort -k2 -n',
            'mkdir grayscale && for img in *.jpg; do convert "$img" -colorspace Gray -resize 50% "grayscale/${img%.*}_gray.jpg"; done && montage grayscale/*_gray.jpg -geometry +5+5 -tile 5x5 collage.jpg && echo "Images processed and collage created"',
            'python -c "import numpy as np; import matplotlib.pyplot as plt; data = np.random.normal(0, 1, 1000); plt.hist(data, bins=30); plt.savefig(\'histogram.png\'); print(f\'Mean: {np.mean(data):.2f}, Std: {np.std(data):.2f}\')" && python -c "import pandas as pd; import seaborn as sns; df = pd.DataFrame(np.random.randn(100, 5), columns=list(\'ABCDE\')); sns.pairplot(df); plt.savefig(\'pairplot.png\')" && echo "Data generated, analyzed, and visualized"',
            'sudo apt update && sudo apt upgrade -y && sudo apt autoremove -y && echo "System updated" && df -h > disk_usage.txt && top -b -n 1 > process_snapshot.txt && cat /var/log/syslog | tail -n 100 > recent_logs.txt && tar -czvf system_report.tar.gz disk_usage.txt process_snapshot.txt recent_logs.txt && echo "System report created" && python -c "import smtplib, ssl; sender=\'sender@example.com\'; receiver=\'receiver@example.com\'; message=\'Subject: System Report\\n\\nPlease find the attached system report.\'; context=ssl.create_default_context(); with smtplib.SMTP_SSL(\'smtp.gmail.com\', 465, context=context) as server: server.login(sender, \'password\'); server.sendmail(sender, receiver, message)" && echo "Report sent via email"'
        ]

        self.create_lab_content(self.lab2, tasks, commands)

    def create_lab_content(self, lab, tasks, commands):
        canvas = tk.Canvas(lab, bg="#ffffff")
        scrollbar = ttk.Scrollbar(lab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for i, (task, command) in enumerate(zip(tasks, commands), 1):
            frame = ttk.Frame(scrollable_frame)
            frame.pack(pady=20, padx=20, fill=tk.X)

            task_label = ttk.Label(frame, text=task, wraplength=900)
            task_label.pack(anchor=tk.W)

            command_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=4, font=('Courier', 12))
            command_text.insert(tk.END, command)
            command_text.pack(fill=tk.X, pady=10)
            command_text.config(state=tk.DISABLED)

            run_button = ttk.Button(frame, text="Run", command=lambda cmd=command: self.run_command(cmd))
            run_button.pack(anchor=tk.E)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def run_command(self, command):
        try:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            self.show_output(result.stdout)
        except subprocess.CalledProcessError as e:
            self.show_output(f"Command failed with error:\n{e.stderr}", error=True)

    def show_output(self, output, error=False):
        output_window = tk.Toplevel(self)
        output_window.title("Command Output")
        output_window.geometry("800x600")

        output_text = scrolledtext.ScrolledText(output_window, wrap=tk.WORD, width=80, height=30, font=('Courier', 12))
        output_text.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        output_text.insert(tk.END, output)
        output_text.config(state=tk.DISABLED)

        if error:
            output_text.config(fg="red")

    def finish(self):
        self.notebook.select(self.lab2)

if __name__ == "__main__":
    app = OneLinerLab()
    app.mainloop()
