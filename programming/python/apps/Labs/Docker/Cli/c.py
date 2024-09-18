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
                ("Create a multi-stage build for a Python Flask application to optimize for minimal image size", 
                 "docker build --no-cache -t flask-app:optimized -f- . <<EOF\nFROM python:3.9-slim as builder\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\nCOPY . .\nFROM python:3.9-slim\nWORKDIR /app\nCOPY --from=builder /app /app\nCMD [\"python\", \"app.py\"]\nEOF"),
                
                ("Deploy a Kubernetes cluster with multiple services, ingress, and persistent volumes using Minikube", 
                 "minikube start && kubectl apply -f https://k8s.io/examples/application/guestbook/redis-leader-deployment.yaml && kubectl apply -f https://k8s.io/examples/application/guestbook/redis-leader-service.yaml && kubectl apply -f https://k8s.io/examples/application/guestbook/redis-follower-deployment.yaml && kubectl apply -f https://k8s.io/examples/application/guestbook/redis-follower-service.yaml && kubectl apply -f https://k8s.io/examples/application/guestbook/frontend-deployment.yaml && kubectl apply -f https://k8s.io/examples/application/guestbook/frontend-service.yaml"),
                
                ("Create a custom Docker network and attach multiple containers for inter-container communication", 
                 "docker network create --driver bridge my_custom_network && docker run -d --name container1 --network my_custom_network alpine sleep 1000 && docker run -d --name container2 --network my_custom_network alpine sleep 1000"),
                
                ("Run a container with resource constraints and custom security options", 
                 "docker run -d --name secure-container --cpu-shares 512 --memory 512m --pids-limit 100 --cap-drop ALL --cap-add NET_BIND_SERVICE --security-opt no-new-privileges alpine sleep 1000"),
                
                ("Set up a Docker Swarm with services, overlay networks, and persistent storage", 
                 "docker swarm init && docker network create --driver overlay my_overlay_network && docker volume create my_volume && docker service create --name my_service --replicas 3 --network my_overlay_network --mount type=volume,source=my_volume,target=/data alpine sleep 1000")
            ]
        else:
            return [
                ("Build and push a multi-architecture Docker image using buildx and QEMU", 
                 "docker run --privileged --rm tonistiigi/binfmt --install all && docker buildx create --name mybuilder --use && docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t myhubuser/myimage:multiarch --push ."),
                
                ("Set up Docker Content Trust and sign images for a secure supply chain", 
                 "export DOCKER_CONTENT_TRUST=1 && docker trust key generate mykey && docker trust signer add --key mykey.pub myname myrepo:mytag && docker push myhubuser/myrepo:mytag"),
                
                ("Create a Docker plugin and enable it for extended Docker functionalities", 
                 "docker plugin create myplugin:latest /path/to/plugin/config.json && docker plugin enable myplugin:latest && docker plugin inspect myplugin:latest"),
                
                ("Use Docker secrets for sensitive data management in a Swarm service", 
                 "echo \"mysecretpassword\" | docker secret create db_password - && docker service create --name mydb --secret db_password -e DB_PASSWORD_FILE=/run/secrets/db_password postgres:13"),
                
                ("Implement Docker health checks and rolling updates for a service", 
                 "docker service create --name myapp --health-cmd \"curl -f http://localhost/health || exit 1\" --health-interval 30s --health-retries 3 --health-timeout 10s myapp:latest && docker service update --image myapp:latest myapp")
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
