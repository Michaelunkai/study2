import tkinter as tk
from tkinter import ttk, scrolledtext
import pyperclip
import subprocess

class OneLinerLab(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Advanced One-Liner Command Lab")
        self.geometry("1200x800")
        self.configure(bg="#000000")
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background="#000000", borderwidth=0)
        style.configure("TNotebook.Tab", background="#333333", foreground="#ffffff", padding=[20, 10], font=('Arial', 12, 'bold'))
        style.map("TNotebook.Tab", background=[("selected", "#666666")])
        
        style.configure("TFrame", background="#000000")
        style.configure("TLabel", background="#000000", foreground="#ffffff", font=('Arial', 14, 'bold'))
        style.configure("TButton", font=('Arial', 12, 'bold'), padding=10, background="#333333", foreground="#ffffff")

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
            "One-Liner to do comprehensive system analysis (uname, lscpu, free, df, lsblk, ip, ss, ps, journalctl, find, lastlog, grep)",
            "One-Liner to automate multi-stage data processing (mkdir, curl, jq, sort, uniq, awk)",
            "One-Liner to implement advanced network security scan (nmap, tcpdump, snort, scapy, python)",
            "One-Liner to execute distributed machine learning task (ssh, curl, python, pandas, sklearn)",
            "One-Liner to orchestrate containerized microservices deployment (docker-compose, kubectl, helm, curl)"
        ]

        commands = [
            'echo "System Analysis Report" > report.txt && uname -a >> report.txt && lscpu >> report.txt && free -h >> report.txt && df -h >> report.txt && lsblk >> report.txt && ip addr show >> report.txt && ss -tuln >> report.txt && ps aux --sort=-%cpu | head -n 11 >> report.txt && journalctl -p err..emerg --since "1 hour ago" >> report.txt && echo "Security Audit" >> report.txt && find / -type f -perm -4000 -ls 2>/dev/null >> report.txt && lastlog >> report.txt && cat /var/log/auth.log | grep -i "failed\|failure" >> report.txt && echo "Report generated successfully" && cat report.txt',
            'mkdir -p data/{raw,processed,final} && for i in {1..5}; do curl -s "https://api.example.com/data?page=$i" > "data/raw/data_$i.json"; done && jq -c ".[] | {id: .id, name: .name, value: .value}" data/raw/*.json | sort | uniq > data/processed/combined.json && awk -F, \'{sum+=$3} END {print "Total Value: " sum}\' data/processed/combined.json > data/final/summary.txt && [ -s data/final/summary.txt ] && echo "Data processing completed successfully" || echo "Error: Data processing failed" >&2',
            'sudo nmap -sS -sV -p- -O --script vuln 192.168.1.0/24 -oN nmap_scan.txt && sudo tcpdump -i eth0 -nn -s0 -v port 80 -w http_traffic.pcap & sleep 300 && kill $! && echo "Network traffic captured" && sudo snort -c /etc/snort/snort.conf -r http_traffic.pcap -l . && cat alert && python3 -c "import scapy.all as scapy; packets = scapy.rdpcap(\'http_traffic.pcap\'); print(f\'Analyzed {len(packets)} packets\'); suspicious = [p for p in packets if p.haslayer(scapy.TCP) and p[scapy.TCP].flags == 2]; print(f\'Found {len(suspicious)} suspicious SYN packets\')"',
            'for node in node1 node2 node3; do ssh $node "mkdir -p ~/ml_task && curl -O https://example.com/dataset.csv && python3 -c \"import pandas as pd; from sklearn.model_selection import train_test_split; from sklearn.ensemble import RandomForestClassifier; df = pd.read_csv(\'dataset.csv\'); X = df.drop(\'target\', axis=1); y = df[\'target\']; X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2); model = RandomForestClassifier(); model.fit(X_train, y_train); print(f\'Accuracy on {node}: {model.score(X_test, y_test):.2f}\')\"" & done && wait && echo "Distributed machine learning task completed"',
            'docker-compose up -d && kubectl create namespace microservices && kubectl apply -f kubernetes-manifests/ && helm install prometheus prometheus-community/prometheus --namespace monitoring --create-namespace && helm install grafana grafana/grafana --namespace monitoring && kubectl get pods --all-namespaces && echo "Microservices deployment completed" && kubectl port-forward svc/grafana 3000:80 -n monitoring & sleep 5 && curl -s http://localhost:3000 > /dev/null && echo "Grafana dashboard is accessible" || echo "Error: Grafana dashboard is not accessible"'
        ]

        self.create_lab_content(self.lab1, tasks, commands)

    def create_lab2(self):
        tasks = [
            "One-Liner to do web scraping and data analysis (scrapy, pandas, matplotlib, sed)",
            "One-Liner to do log analysis and anomaly detection (logwatch, grep, awk, python, pandas, sklearn)",
            "One-Liner to do database maintenance (psql, vacuumdb, reindexdb, pg_dump)",
            "One-Liner to do CI/CD pipeline (git, npm, docker, kubectl)",
            "One-Liner to do cloud infrastructure deployment (terraform, aws, kubectl, helm)"
        ]

        commands = [
            'pip install scrapy pandas matplotlib && scrapy startproject webscraper && cd webscraper && scrapy genspider example example.com && sed -i \'s/pass/import scrapy\\n    def parse(self, response):\\n        for product in response.css(".product"):\\n            yield {\\n                "name": product.css("h2::text").get(),\\n                "price": product.css(".price::text").get(),\\n                "url": product.css("a::attr(href)").get()\\n            }/\' webscraper/spiders/example.py && scrapy crawl example -o products.json && python3 -c "import pandas as pd; import matplotlib.pyplot as plt; df = pd.read_json(\'products.json\'); plt.figure(figsize=(10,6)); plt.scatter(df[\'name\'], df[\'price\']); plt.xticks(rotation=90); plt.tight_layout(); plt.savefig(\'price_distribution.png\'); print(f\'Average price: {df[\'price\'].mean():.2f}\')"',
            'sudo apt install -y logwatch && logwatch --detail High --range All --format text > logwatch_report.txt && grep -E "Failed password|Invalid user" /var/log/auth.log | awk \'{print $9}\' | sort | uniq -c | sort -nr > failed_logins.txt && python3 -c "import pandas as pd; from sklearn.ensemble import IsolationForest; df = pd.read_csv(\'failed_logins.txt\', sep=\' \', names=[\'count\', \'ip\']); model = IsolationForest(contamination=0.1); df[\'anomaly\'] = model.fit_predict(df[[\'count\']]); print(df[df[\'anomaly\'] == -1])" > anomalies.txt && echo "Log analysis completed. Check logwatch_report.txt, failed_logins.txt, and anomalies.txt for results."',
            'sudo -u postgres psql -c "SELECT pg_database.datname, pg_size_pretty(pg_database_size(pg_database.datname)) AS size FROM pg_database;" > db_sizes.txt && sudo -u postgres psql -c "SELECT schemaname, relname, n_live_tup, n_dead_tup, last_vacuum, last_autovacuum FROM pg_stat_user_tables ORDER BY n_dead_tup DESC LIMIT 10;" > table_stats.txt && sudo -u postgres vacuumdb --all --analyze-in-stages && sudo -u postgres reindexdb --all && sudo -u postgres pg_dump -C -w -F tar -f backup.tar postgres && echo "Database maintenance completed. Check db_sizes.txt and table_stats.txt for details."',
            'git clone https://github.com/example/repo.git && cd repo && npm install && npm test && npm run lint && npm audit && docker build -t myapp:latest . && docker scan myapp:latest && kubectl create secret docker-registry regcred --docker-server=<your-registry-server> --docker-username=<your-name> --docker-password=<your-pword> --docker-email=<your-email> && kubectl apply -f k8s-manifests/ && kubectl rollout status deployment/myapp && kubectl get services -o wide | grep myapp',
            'terraform init && terraform plan -out=tfplan && terraform apply tfplan && aws cloudformation create-stack --stack-name monitoring-stack --template-body file://cloudformation-template.yaml --capabilities CAPABILITY_IAM && aws eks --region us-west-2 update-kubeconfig --name my-cluster && kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml && helm repo add prometheus-community https://prometheus-community.github.io/helm-charts && helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --create-namespace && kubectl port-forward svc/prometheus-grafana 3000:80 -n monitoring & echo "Infrastructure deployed and monitoring set up. Access Grafana dashboard at http://localhost:3000"'
        ]

        self.create_lab_content(self.lab2, tasks, commands)

    def create_lab_content(self, lab, tasks, commands):
        canvas = tk.Canvas(lab, bg="#000000")
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

            task_label = ttk.Label(frame, text=task, wraplength=1100)
            task_label.pack(anchor=tk.W)
            task_label.bind("<Double-1>", lambda e, t=task: self.copy_to_clipboard(t))

            command_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=100, height=6, font=('Courier', 12), bg="#1c1c1c", fg="#ffffff")
            command_text.insert(tk.END, command)
            command_text.pack(fill=tk.X, pady=10)
            command_text.config(state=tk.DISABLED)
            command_text.bind("<Double-1>", lambda e, c=command: self.copy_to_clipboard(c))

            run_button = ttk.Button(frame, text="Run", command=lambda cmd=command: self.run_command(cmd))
            run_button.pack(anchor=tk.E)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def copy_to_clipboard(self, text):
        pyperclip.copy(text)
        print("Copied to clipboard:", text[:50] + "..." if len(text) > 50 else text)

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
        output_window.configure(bg="#000000")

        output_text = scrolledtext.ScrolledText(output_window, wrap=tk.WORD, width=80, height=30, font=('Courier', 12), bg="#1c1c1c", fg="#ffffff")
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
