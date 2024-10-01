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
                ("Create a Docker network for two containers to communicate", 
                 "docker network create --driver bridge my_bridge && docker run -d --name container1 --network my_bridge alpine sleep 1000 && docker run -d --name container2 --network my_bridge alpine sleep 1000"),
                
                ("Build and run a Docker container from a simple Dockerfile", 
                 "echo -e 'FROM alpine:latest\\nCMD [\"echo\", \"Hello World\"]' > Dockerfile && docker build -t hello-world . && docker run hello-world"),
                
                ("Create a Docker volume and use it in a container", 
                 "docker volume create my_volume && docker run -d --name my_container -v my_volume:/data alpine sleep 1000 && docker exec my_container sh -c 'echo Hello > /data/hello.txt'"),
                
                ("Run a Docker container with environment variables", 
                 "docker run -d --name env_container -e MY_VAR=HelloWorld alpine sh -c 'while true; do echo $MY_VAR; sleep 1; done'"),
                
                ("Pull an image from Docker Hub and run it", 
                 "docker pull nginx:alpine && docker run -d --name my_nginx -p 8080:80 nginx:alpine")
            ]
        else:
            return [
                ("Build and push a Docker image to Docker Hub", 
                 "echo -e 'FROM alpine:latest\\nCMD [\"echo\", \"Pushed to Docker Hub\"]' > Dockerfile && docker build -t myhubuser/myimage . && docker login && docker push myhubuser/myimage"),
                
                ("Run a Docker container with a mounted host directory", 
                 "docker run -d --name mounted_container -v /path/on/host:/path/in/container alpine sleep 1000"),
                
                ("Create and use Docker secrets", 
                 "echo \"my_secret\" | docker secret create my_secret - && docker service create --name secret_service --secret my_secret alpine sleep 1000"),
                
                ("Run a Docker container with custom DNS settings", 
                 "docker run -d --name dns_container --dns 8.8.8.8 --dns-search example.com alpine sleep 1000"),
                
                ("Use Docker Compose to define and run a multi-container application", 
                 "echo -e 'version: \"3\"\\nservices:\\n  web:\\n    image: nginx:alpine\\n    ports:\\n      - \"80:80\"\\n  redis:\\n    image: redis:alpine' > docker-compose.yml && docker-compose up -d")
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
