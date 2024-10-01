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
        self.master.geometry("1400x900")
        self.master.configure(bg="#2e2e2e")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background="#2e2e2e", borderwidth=0)
        style.configure("TNotebook.Tab", background="#3c3c3c", foreground="#e0e0e0", padding=[10, 5], font=("Arial", 12, "bold"))
        style.map("TNotebook.Tab", background=[("selected", "#1e90ff")], foreground=[("selected", "#ffffff")])

        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill="both", padx=20, pady=20)

        self.tasks = [
            {
                "name": "Create a Serverless API",
                "gcloud": {
                    "command": "gcloud functions deploy my-function --runtime nodejs14 --trigger-http --allow-unauthenticated",
                    "service": "Google Cloud Functions",
                    "output": "Deploying function...done.\nService URL: https://region-project.cloudfunctions.net/my-function"
                },
                "azure": {
                    "command": "az functionapp create --resource-group myResourceGroup --consumption-plan-location westeurope --runtime node --functions-version 3 --name myFunctionApp --storage-account mystorageaccount",
                    "service": "Azure Functions",
                    "output": "Function app created.\nURL: https://myFunctionApp.azurewebsites.net"
                },
                "aws": {
                    "command": "aws lambda create-function --function-name my-function --runtime nodejs14.x --role arn:aws:iam::123456789012:role/execution_role --handler index.handler --code S3Bucket=my-bucket,S3Key=function.zip",
                    "service": "AWS Lambda",
                    "output": "Function created successfully.\nARN: arn:aws:lambda:us-west-2:123456789012:function:my-function"
                }
            },
            {
                "name": "Deploy a Containerized App",
                "gcloud": {
                    "command": "gcloud run deploy my-app --image gcr.io/my-project/my-app --platform managed",
                    "service": "Google Cloud Run",
                    "output": "Deploying container...done.\nService URL: https://my-app-a12b3c4d5e6-uc.a.run.app"
                },
                "azure": {
                    "command": "az container create --resource-group myResourceGroup --name myContainer --image myacr.azurecr.io/my-app:latest --dns-name-label my-app",
                    "service": "Azure Container Instances",
                    "output": "Container created successfully.\nURL: http://my-app.westeurope.azurecontainer.io"
                },
                "aws": {
                    "command": "aws ecs create-service --cluster my-cluster --service-name my-service --task-definition my-task-def --desired-count 1 --launch-type FARGATE",
                    "service": "Amazon ECS",
                    "output": "Service created successfully.\nService ARN: arn:aws:ecs:us-west-2:123456789012:service/my-service"
                }
            },
            {
                "name": "Set Up a CI/CD Pipeline",
                "gcloud": {
                    "command": "gcloud builds submit --tag gcr.io/my-project/my-app && gcloud beta run deploy my-app --image gcr.io/my-project/my-app --platform managed",
                    "service": "Google Cloud Build & Run",
                    "output": "Build and deployment triggered.\nService URL: https://my-app-a12b3c4d5e6-uc.a.run.app"
                },
                "azure": {
                    "command": "az pipelines create --name myPipeline --repository myRepo --branch main --yml-path /azure-pipelines.yml",
                    "service": "Azure Pipelines",
                    "output": "Pipeline created successfully.\nURL: https://dev.azure.com/myProject/_build"
                },
                "aws": {
                    "command": "aws codepipeline create-pipeline --cli-input-json file://pipeline.json",
                    "service": "AWS CodePipeline",
                    "output": "Pipeline created successfully.\nPipeline ARN: arn:aws:codepipeline:us-west-2:123456789012:my-pipeline"
                }
            },
            {
                "name": "Create a Managed Database",
                "gcloud": {
                    "command": "gcloud sql instances create my-instance --database-version=MYSQL_5_7 --tier=db-f1-micro --region=us-central1",
                    "service": "Google Cloud SQL",
                    "output": "Creating Cloud SQL instance...done.\nInstance created successfully."
                },
                "azure": {
                    "command": "az sql server create --name myServer --resource-group myResourceGroup --location westeurope --admin-user myAdmin --admin-password myPassword && az sql db create --resource-group myResourceGroup --server myServer --name myDatabase --service-objective S0",
                    "service": "Azure SQL Database",
                    "output": "SQL Server and Database created successfully.\nServer: myServer\nDatabase: myDatabase"
                },
                "aws": {
                    "command": "aws rds create-db-instance --db-instance-identifier mydbinstance --db-instance-class db.t2.micro --engine mysql --master-username admin --master-user-password password --allocated-storage 20",
                    "service": "Amazon RDS",
                    "output": "Creating RDS instance...done.\nInstance created successfully."
                }
            },
            {
                "name": "Set Up Object Storage",
                "gcloud": {
                    "command": "gsutil mb -l us-central1 gs://my-bucket && gsutil cp ./my-file gs://my-bucket",
                    "service": "Google Cloud Storage",
                    "output": "Bucket and file created successfully."
                },
                "azure": {
                    "command": "az storage account create --name mystorageaccount --resource-group myResourceGroup --location westeurope --sku Standard_LRS && az storage container create --name my-container --account-name mystorageaccount && az storage blob upload --container-name my-container --file ./my-file --name my-blob",
                    "service": "Azure Blob Storage",
                    "output": "Storage account, container, and blob created successfully."
                },
                "aws": {
                    "command": "aws s3 mb s3://my-bucket && aws s3 cp ./my-file s3://my-bucket",
                    "service": "Amazon S3",
                    "output": "Bucket and file created successfully."
                }
            }
        ]

        self.create_task_tabs()

        self.finish_button = tk.Button(self.master, text="Finish", command=self.open_new_lab, bg="#1e90ff", fg="white", font=("Arial", 14, "bold"))
        self.finish_button.pack(pady=20)

    def create_task_tabs(self):
        for task in self.tasks:
            tab = ttk.Frame(self.notebook, style="TNotebook")
            self.notebook.add(tab, text=task["name"])

            for cloud, details in [("Google Cloud", task["gcloud"]), ("Azure", task["azure"]), ("AWS", task["aws"])]:
                frame = tk.Frame(tab, bg="#2e2e2e")
                frame.pack(fill=tk.X, padx=20, pady=10)

                cloud_label = tk.Label(frame, text=f"{cloud}:", font=("Arial", 16, "bold"), bg="#2e2e2e", fg="#1e90ff")
                cloud_label.pack(anchor="w")
                cloud_label.bind("<Double-Button-1>", lambda e, task_name=task["name"]: self.copy_task_to_clipboard(task_name))

                service_label = tk.Label(frame, text=f"Service: {details['service']}", font=("Arial", 12, "italic"), bg="#2e2e2e", fg="#ffffff")
                service_label.pack(anchor="w")
                service_label.bind("<Double-Button-1>", lambda e, task_name=task["name"]: self.copy_task_to_clipboard(task_name))

                command_text = tk.Text(frame, height=4, wrap=tk.WORD, font=("Courier", 12), bg="#3c3c3c", fg="#ffffff", insertbackground="white")
                command_text.insert(tk.END, details["command"])
                command_text.config(state=tk.DISABLED)
                command_text.pack(fill=tk.X, pady=5)
                command_text.bind("<Double-Button-1>", lambda e, text=details["command"]: self.copy_to_clipboard(text))

                run_button = tk.Button(frame, text="Run Command", command=lambda cmd=details["command"], output=details["output"]: self.run_command(cmd, output), bg="#1e90ff", fg="white", font=("Arial", 12, "bold"))
                run_button.pack(pady=5)

    def copy_task_to_clipboard(self, task_name):
        task_text = f"n '{task_name}'"
        pyperclip.copy(task_text)
        print(f"Copied to clipboard: {task_text}")

    def copy_to_clipboard(self, text):
        pyperclip.copy(text)
        print("Copied to clipboard:", text)

    def run_command(self, command, output):
        output_window = tk.Toplevel(self.master)
        output_window.title("Command Output")
        output_window.geometry("800x600")
        output_window.configure(bg="#2e2e2e")

        output_text = tk.Text(output_window, wrap=tk.WORD, font=("Courier", 12), bg="#3c3c3c", fg="#ffffff", insertbackground="white")
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
