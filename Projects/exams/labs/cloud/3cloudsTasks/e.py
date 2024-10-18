import tkinter as tk
from tkinter import ttk
import threading
import pyperclip
import random
import time

class CloudCLILab:
    def __init__(self, master):
        self.master = master
        self.master.title("Cloud CLI Lab")
        self.master.geometry("1200x800")
        self.master.configure(bg="black")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background="black", borderwidth=0)
        style.configure("TNotebook.Tab", background="black", foreground="white", padding=[10, 5])
        style.map("TNotebook.Tab", background=[("selected", "gray25")])

        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill="both", padx=20, pady=20)

        self.tasks = [
            {
                "name": "Deploy a Static Website",
                "gcloud": {
                    "command": "gsutil mb -l us-central1 gs://my-static-website && gsutil cp -r ./website/* gs://my-static-website && gsutil web set -m index.html -e 404.html gs://my-static-website",
                    "service": "Google Cloud Storage",
                    "output": "Creating gs://my-static-website/...\nCopying file://./website/index.html [Content-Type=text/html]...\nCopying file://./website/404.html [Content-Type=text/html]...\nSetting website configuration on gs://my-static-website/..."
                },
                "azure": {
                    "command": "az storage account create --name mystorageaccount --resource-group myResourceGroup --location eastus --sku Standard_LRS && az storage container create --name $web --account-name mystorageaccount && az storage blob upload-batch --destination $web --source ./website",
                    "service": "Azure Blob Storage",
                    "output": "{\n  \"created\": true\n}\n{\n  \"container\": \"$web\"\n}\nUploading index.html to $web in mystorageaccount...\nUploading 404.html to $web in mystorageaccount..."
                },
                "aws": {
                    "command": "aws s3 mb s3://my-static-website --region us-east-1 && aws s3 cp --recursive ./website s3://my-static-website/ && aws s3 website s3://my-static-website/ --index-document index.html --error-document 404.html",
                    "service": "Amazon S3",
                    "output": "make_bucket: my-static-website\nupload: ./website/index.html to s3://my-static-website/index.html\nupload: ./website/404.html to s3://my-static-website/404.html\nWebsite configuration applied to bucket: my-static-website"
                }
            },
            {
                "name": "Create a Virtual Machine",
                "gcloud": {
                    "command": "gcloud compute instances create my-vm --zone=us-central1-a --machine-type=e2-medium --image-family=debian-9 --image-project=debian-cloud",
                    "service": "Google Compute Engine",
                    "output": "Created [https://www.googleapis.com/compute/v1/projects/my-project/zones/us-central1-a/instances/my-vm].\nNAME  ZONE           MACHINE_TYPE  PREEMPTIBLE  INTERNAL_IP  EXTERNAL_IP  STATUS\nmy-vm  us-central1-a  e2-medium                  10.128.0.2   35.238.1.1   RUNNING"
                },
                "azure": {
                    "command": "az vm create --resource-group myResourceGroup --name myVM --image UbuntuLTS --admin-username azureuser --generate-ssh-keys",
                    "service": "Azure Virtual Machines",
                    "output": "{\n  \"fqdns\": \"\",\n  \"id\": \"/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myResourceGroup/providers/Microsoft.Compute/virtualMachines/myVM\",\n  \"location\": \"eastus\",\n  \"powerState\": \"VM running\",\n  \"privateIpAddress\": \"10.0.0.4\",\n  \"publicIpAddress\": \"20.30.40.50\",\n  \"resourceGroup\": \"myResourceGroup\",\n  \"zones\": \"\"\n}"
                },
                "aws": {
                    "command": "aws ec2 run-instances --image-id ami-0abcdef1234567890 --count 1 --instance-type t2.micro --key-name MyKeyPair --security-group-ids sg-12345678 --subnet-id subnet-6e7f829e",
                    "service": "Amazon EC2",
                    "output": "{\n  \"Instances\": [\n    {\n      \"InstanceId\": \"i-1234567890abcdef0\",\n      \"ImageId\": \"ami-0abcdef1234567890\",\n      \"InstanceType\": \"t2.micro\",\n      \"State\": {\n        \"Code\": 0,\n        \"Name\": \"pending\"\n      },\n      \"PrivateIpAddress\": \"10.0.0.1\",\n      \"PublicIpAddress\": \"54.123.45.67\"\n    }\n  ]\n}"
                }
            },
            {
                "name": "Set Up a Database",
                "gcloud": {
                    "command": "gcloud sql instances create my-instance --database-version=POSTGRES_12 --tier=db-f1-micro --region=us-central1 && gcloud sql users set-password postgres --instance=my-instance --password=my-password",
                    "service": "Google Cloud SQL",
                    "output": "Creating Cloud SQL instance...done.\nCreated [https://www.googleapis.com/sql/v1beta4/projects/my-project/instances/my-instance].\nSetting password for user [postgres] in instance [my-instance]...done."
                },
                "azure": {
                    "command": "az sql server create --name myserver --resource-group myResourceGroup --location eastus --admin-user myadmin --admin-password myPassword123 && az sql db create --resource-group myResourceGroup --server myserver --name myDatabase --service-objective S0",
                    "service": "Azure SQL Database",
                    "output": "{\n  \"fullyQualifiedDomainName\": \"myserver.database.windows.net\",\n  \"administratorLogin\": \"myadmin\",\n  \"version\": \"12.0\"\n}\n{\n  \"databaseName\": \"myDatabase\",\n  \"edition\": \"Standard\",\n  \"status\": \"Online\"\n}"
                },
                "aws": {
                    "command": "aws rds create-db-instance --db-instance-identifier mydatabase --db-instance-class db.t2.micro --engine postgres --master-username admin --master-user-password mypassword --allocated-storage 20",
                    "service": "Amazon RDS",
                    "output": "{\n  \"DBInstanceIdentifier\": \"mydatabase\",\n  \"DBInstanceStatus\": \"creating\",\n  \"Engine\": \"postgres\",\n  \"MasterUsername\": \"admin\",\n  \"AllocatedStorage\": 20\n}"
                }
            }
        ]

        self.create_task_tabs()

        self.finish_button = tk.Button(self.master, text="Finish", command=self.open_new_lab, bg="gray25", fg="white", font=("Arial", 14, "bold"))
        self.finish_button.pack(pady=20)

    def create_task_tabs(self):
        for task in self.tasks:
            tab = ttk.Frame(self.notebook, style="TNotebook")
            self.notebook.add(tab, text=task["name"])

            for cloud, details in [("Google Cloud", task["gcloud"]), ("Azure", task["azure"]), ("AWS", task["aws"])]:
                frame = tk.Frame(tab, bg="black")
                frame.pack(fill=tk.X, padx=20, pady=10)

                cloud_label = tk.Label(frame, text=f"{cloud}:", font=("Arial", 16, "bold"), bg="black", fg="white")
                cloud_label.pack(anchor="w")
                cloud_label.bind("<Double-Button-1>", lambda e, text=details["service"]: self.copy_to_clipboard(text))

                service_label = tk.Label(frame, text=f"Service: {details['service']}", font=("Arial", 12, "italic"), bg="black", fg="white")
                service_label.pack(anchor="w")
                service_label.bind("<Double-Button-1>", lambda e, text=details["service"]: self.copy_to_clipboard(text))

                command_text = tk.Text(frame, height=4, wrap=tk.WORD, font=("Courier", 12), bg="gray10", fg="white", insertbackground="white")
                command_text.insert(tk.END, details["command"])
                command_text.config(state=tk.DISABLED)
                command_text.pack(fill=tk.X, pady=5)
                command_text.bind("<Double-Button-1>", lambda e, text=details["command"]: self.copy_to_clipboard(text))

                run_button = tk.Button(frame, text="Run Command", command=lambda cmd=details["command"], output=details["output"]: self.run_command(cmd, output), bg="gray25", fg="white", font=("Arial", 12, "bold"))
                run_button.pack(pady=5)

    def copy_to_clipboard(self, text):
        pyperclip.copy(text)
        print("Copied to clipboard:", text)

    def run_command(self, command, output):
        output_window = tk.Toplevel(self.master)
        output_window.title("Command Output")
        output_window.geometry("800x600")
        output_window.configure(bg="black")

        output_text = tk.Text(output_window, wrap=tk.WORD, font=("Courier", 12), bg="black", fg="white", insertbackground="white")
        output_text.pack(expand=True, fill="both", padx=20, pady=20)

        def simulate_output():
            output_text.insert(tk.END, f"Executing command: {command}\n\n")
            output_text.update()
            time.sleep(2)  # Simulate some processing time
            
            # Simulate a gradual output
            lines = output.split('\n')
            for line in lines:
                output_text.insert(tk.END, line + '\n')
                output_text.see(tk.END)
                output_text.update()
                time.sleep(0.1 + random.random() * 0.3)  # Random delay between lines
            
            output_text.insert(tk.END, "\nCommand execution completed.")
            output_text.config(state=tk.DISABLED)

        threading.Thread(target=simulate_output).start()

    def open_new_lab(self):
        new_window = tk.Toplevel(self.master)
        new_lab = CloudCLILab(new_window)
        # You can define new tasks here if needed, or it will use the same tasks

if __name__ == "__main__":
    root = tk.Tk()
    app = CloudCLILab(root)
    root.mainloop()
