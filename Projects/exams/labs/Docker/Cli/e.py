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
                ("Run a containerized Apache HTTP server and access the default page", 
                 "docker run -d --name apache-server -p 8080:80 httpd:alpine && docker exec -it apache-server sh -c 'echo \"Server running...\" && exec sh'"),
                
                ("Run a container with Node.js and start a simple Express.js server", 
                 "docker run -d --name node-server -p 3000:3000 -v $(pwd)/app:/app -w /app node:alpine sh -c 'npm init -y && npm install express && node -e \"require('express')().get('/', (req, res) => res.send('Hello World')).listen(3000)\"' && docker exec -it node-server sh"),
                
                ("Run a MongoDB container with persistent data storage", 
                 "docker run -d --name mongodb-container -p 27017:27017 -v mongo_data:/data/db mongo && docker exec -it mongodb-container mongo"),
                
                ("Run a PostgreSQL container with a custom database and user", 
                 "docker run -d --name postgres-container -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=mydb -p 5432:5432 postgres && docker exec -it postgres-container psql -U myuser -d mydb"),
                
                ("Run a Python Flask application in a container", 
                 "docker run -d --name flask-app -p 5000:5000 -v $(pwd)/app:/app -w /app python:alpine sh -c 'pip install flask && echo \"from flask import Flask; app = Flask(__name__); @app.route('/') def home(): return 'Hello from Flask'; if __name__ == '__main__': app.run(host='0.0.0.0')\" > app.py && python app.py'")
            ]
        else:
            return [
                ("Run a WordPress site with MySQL database using Docker Compose", 
                 "docker-compose -f- up -d <<EOF\nversion: '3.3'\nservices:\n  db:\n    image: mysql:5.7\n    volumes:\n      - db_data:/var/lib/mysql\n    restart: always\n    environment:\n      MYSQL_ROOT_PASSWORD: somewordpress\n      MYSQL_DATABASE: wordpress\n      MYSQL_USER: wordpress\n      MYSQL_PASSWORD: wordpress\n  wordpress:\n    depends_on:\n      - db\n    image: wordpress:latest\n    volumes:\n      - wordpress_data:/var/www/html\n    ports:\n      - '8080:80'\n    restart: always\n    environment:\n      WORDPRESS_DB_HOST: db:3306\n      WORDPRESS_DB_USER: wordpress\n      WORDPRESS_DB_PASSWORD: wordpress\n      WORDPRESS_DB_NAME: wordpress\nvolumes:\n  db_data:\n  wordpress_data:\nEOF && docker exec -it $(docker-compose ps -q wordpress) bash"),
                
                ("Run a Jenkins container and configure it using a Groovy script", 
                 "docker run -d --name jenkins-container -p 8080:8080 -p 50000:50000 -v jenkins_data:/var/jenkins_home jenkins/jenkins:lts && docker exec -it jenkins-container sh -c 'echo \"println 'Jenkins configured'\" > /usr/share/jenkins/ref/init.groovy.d/basic-security.groovy'"),
                
                ("Run a GitLab CE container with external storage for Git repositories", 
                 "docker run -d --name gitlab-container -p 443:443 -p 80:80 -p 22:22 -v gitlab_data:/var/opt/gitlab -v gitlab_logs:/var/log/gitlab -v gitlab_config:/etc/gitlab gitlab/gitlab-ce:latest && docker exec -it gitlab-container gitlab-ctl reconfigure"),
                
                ("Run an ELK stack (Elasticsearch, Logstash, Kibana) using Docker Compose", 
                 "docker-compose -f- up -d <<EOF\nversion: '3'\nservices:\n  elasticsearch:\n    image: docker.elastic.co/elasticsearch/elasticsearch:7.10.1\n    environment:\n      - node.name=es01\n      - discovery.type=single-node\n    ports:\n      - 9200:9200\n      - 9300:9300\n  logstash:\n    image: docker.elastic.co/logstash/logstash:7.10.1\n    ports:\n      - 5044:5044\n    environment:\n      - xpack.monitoring.enabled=false\n  kibana:\n    image: docker.elastic.co/kibana/kibana:7.10.1\n    ports:\n      - 5601:5601\nEOF && docker exec -it $(docker-compose ps -q kibana) bash"),
                
                ("Run a Nextcloud container with MariaDB backend", 
                 "docker-compose -f- up -d <<EOF\nversion: '3'\nservices:\n  db:\n    image: mariadb\n    volumes:\n      - db_data:/var/lib/mysql\n    restart: always\n    environment:\n      MYSQL_ROOT_PASSWORD: example\n      MYSQL_DATABASE: nextcloud\n      MYSQL_USER: nextcloud\n      MYSQL_PASSWORD: example\n  app:\n    image: nextcloud\n    ports:\n      - 8080:80\n    links:\n      - db\n    volumes:\n      - nextcloud_data:/var/www/html\nvolumes:\n  db_data:\n  nextcloud_data:\nEOF && docker exec -it $(docker-compose ps -q app) bash")
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
