import tkinter as tk
from tkinter import font, scrolledtext
import pyperclip
import textwrap
import random
import time

class DockerCLILab:
    def __init__(self, master):
        self.master = master
        self.master.title("Advanced Docker CLI Lab")
        self.master.configure(bg="black")
        
        # Get screen width and height
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        
        # Calculate window size (50% of screen width, full height)
        window_width = screen_width // 2
        window_height = screen_height
        
        # Set window size and position (align to left side of screen)
        self.master.geometry(f"{window_width}x{window_height}+0+0")

        self.current_lab = 1
        self.create_widgets()

    def create_widgets(self):
        self.style()
        
        self.title_label = tk.Label(self.master, text=f"Docker CLI Lab {self.current_lab}", font=self.title_font, bg="black", fg="white")
        self.title_label.pack(pady=10)

        self.canvas = tk.Canvas(self.master, bg="black", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="black")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.tasks = self.get_tasks()

        for task, command in self.tasks:
            task_label = tk.Label(self.scrollable_frame, text=task, font=self.task_font, bg="black", fg="white", wraplength=self.master.winfo_width() - 40, justify="left")
            task_label.pack(anchor="w", pady=(10, 5))
            task_label.bind("<Double-Button-1>", lambda e, t=task: self.copy_to_clipboard(t))

            command_text = tk.Text(self.scrollable_frame, wrap=tk.WORD, width=60, height=3, font=self.command_font, bg="#1E1E1E", fg="#D4D4D4", insertbackground="white")
            command_text.insert(tk.END, textwrap.fill(command, width=60))
            command_text.config(state="disabled")
            command_text.pack(pady=5)
            command_text.bind("<Double-Button-1>", lambda e, c=command: self.copy_to_clipboard(c))

            run_button = tk.Button(self.scrollable_frame, text="Run", command=lambda cmd=command: self.simulate_command(cmd), font=self.button_font, bg="#0D47A1", fg="white", activebackground="#1565C0", activeforeground="white")
            run_button.pack(pady=(0, 5))

        self.finish_button = tk.Button(self.master, text="Finish", command=self.finish_lab, font=self.button_font, bg="#388E3C", fg="white", activebackground="#43A047", activeforeground="white")
        self.finish_button.pack(pady=10)

    def style(self):
        self.title_font = font.Font(family="Arial", size=18, weight="bold")
        self.task_font = font.Font(family="Arial", size=12, weight="bold")
        self.command_font = font.Font(family="Consolas", size=10)
        self.button_font = font.Font(family="Arial", size=10, weight="bold")

    def get_tasks(self):
        if self.current_lab == 1:
            return [
                ("Run a PostgreSQL container and access the PostgreSQL shell", 
                 "docker run -d --name postgres-container -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 postgres:13 && docker exec -it postgres-container psql -U postgres"),
                
                ("Run a MySQL container and access the MySQL shell", 
                 "docker run -d --name mysql-container -e MYSQL_ROOT_PASSWORD=mysecretpassword -p 3306:3306 mysql:8.0 && docker exec -it mysql-container mysql -u root -p"),
                
                ("Run an Nginx container and access the Nginx logs", 
                 "docker run -d --name nginx-container -p 8080:80 nginx && docker exec -it nginx-container tail -f /var/log/nginx/access.log"),
                
                ("Run a Redis container and access the Redis CLI", 
                 "docker run -d --name redis-container -p 6379:6379 redis && docker exec -it redis-container redis-cli"),
                
                ("Run a Jenkins container and access the Jenkins CLI", 
                 "docker run -d --name jenkins-container -p 8080:8080 -p 50000:50000 jenkins/jenkins:lts && docker exec -it jenkins-container /bin/bash")
            ]
        else:
            return [
                ("Run a MongoDB container and access the MongoDB shell", 
                 "docker run -d --name mongodb-container -p 27017:27017 mongo && docker exec -it mongodb-container mongo"),
                
                ("Run an Elasticsearch container and access the Elasticsearch logs", 
                 "docker run -d --name elasticsearch-container -p 9200:9200 -p 9300:9300 elasticsearch:7.10.1 && docker exec -it elasticsearch-container tail -f /usr/share/elasticsearch/logs/elasticsearch.log"),
                
                ("Run a RabbitMQ container and access the RabbitMQ management console", 
                 "docker run -d --name rabbitmq-container -p 5672:5672 -p 15672:15672 rabbitmq:management && docker exec -it rabbitmq-container rabbitmqctl status"),
                
                ("Run a SonarQube container and access the SonarQube logs", 
                 "docker run -d --name sonarqube-container -p 9000:9000 sonarqube && docker exec -it sonarqube-container tail -f /opt/sonarqube/logs/sonar.log"),
                
                ("Run a Grafana container and access the Grafana logs", 
                 "docker run -d --name grafana-container -p 3000:3000 grafana/grafana && docker exec -it grafana-container tail -f /var/log/grafana/grafana.log")
            ]

    def copy_to_clipboard(self, text):
        pyperclip.copy(text)

    def simulate_command(self, command):
        output_window = tk.Toplevel(self.master)
        output_window.title("Command Output")
        output_window.geometry("600x400")
        output_window.configure(bg="black")

        output_text = scrolledtext.ScrolledText(output_window, wrap=tk.WORD, width=70, height=20, font=self.command_font, bg="#1E1E1E", fg="#D4D4D4", insertbackground="white")
        output_text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        output_text.insert(tk.END, f"Running command: {command}\n\n")
        output_text.update()

        # Simulate command execution
        for _ in range(random.randint(5, 15)):
            output_line = f"{random.choice(['INFO', 'DEBUG', 'WARN'])}: {self.generate_random_output()}\n"
            output_text.insert(tk.END, output_line)
            output_text.see(tk.END)
            output_text.update()
            time.sleep(0.5)

        output_text.insert(tk.END, "\nCommand completed successfully.")
        output_text.config(state="disabled")

    def generate_random_output(self):
        outputs = [
            "Processing files...",
            "Downloading dependencies...",
            "Building image layers...",
            "Pushing to registry...",
            "Configuring network interfaces...",
            "Applying security policies...",
            "Initializing volumes...",
            "Starting containers...",
            "Updating service configurations...",
            "Performing health checks..."
        ]
        return random.choice(outputs)

    def finish_lab(self):
        if self.current_lab == 1:
            self.current_lab = 2
            self.scrollable_frame.destroy()
            self.canvas.destroy()
            self.scrollbar.destroy()
            self.finish_button.destroy()
            self.title_label.destroy()
            self.create_widgets()
        else:
            self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = DockerCLILab(root)
    root.mainloop()
