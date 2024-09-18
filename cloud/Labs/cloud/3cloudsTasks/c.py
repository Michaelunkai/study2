import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import pyperclip
import platform

class CloudCLILab:
    def __init__(self, master):
        self.master = master
        self.master.title("Cloud CLI Lab")
        self.master.geometry("1000x800")
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
                "name": "Create a Serverless API",
                "gcloud": {
                    "command": "gcloud functions deploy hello-world --runtime python39 --trigger-http --allow-unauthenticated",
                    "service": "Cloud Functions"
                },
                "azure": {
                    "command": "az functionapp create --resource-group myResourceGroup --consumption-plan-location eastus --runtime python --name my-api-app --storage-account mystorageaccount",
                    "service": "Azure Functions"
                },
                "aws": {
                    "command": "aws lambda create-function --function-name my-api --runtime python3.9 --role arn:aws:iam::123456789012:role/lambda-role --handler lambda_function.handler --zip-file fileb://function.zip",
                    "service": "AWS Lambda"
                }
            },
            {
                "name": "Set Up a Managed Kubernetes Cluster",
                "gcloud": {
                    "command": "gcloud container clusters create my-cluster --zone us-central1-a --num-nodes 3 --enable-autoscaling --min-nodes 1 --max-nodes 5",
                    "service": "Google Kubernetes Engine (GKE)"
                },
                "azure": {
                    "command": "az aks create --resource-group myResourceGroup --name myAKSCluster --node-count 3 --enable-addons monitoring --generate-ssh-keys --enable-cluster-autoscaler --min-count 1 --max-count 5",
                    "service": "Azure Kubernetes Service (AKS)"
                },
                "aws": {
                    "command": "eksctl create cluster --name my-cluster --region us-west-2 --nodes 3 --nodes-min 1 --nodes-max 5 --asg-access",
                    "service": "Amazon Elastic Kubernetes Service (EKS)"
                }
            },
            {
                "name": "Deploy a Scalable Web Application",
                "gcloud": {
                    "command": "gcloud run deploy --image gcr.io/my-project/my-app --platform managed --allow-unauthenticated",
                    "service": "Cloud Run"
                },
                "azure": {
                    "command": "az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name my-web-app --deployment-container-image-name myacr.azurecr.io/my-app:latest",
                    "service": "Azure App Service"
                },
                "aws": {
                    "command": "aws ecs create-service --cluster my-cluster --service-name my-web-app --task-definition my-task-def --desired-count 3 --launch-type FARGATE",
                    "service": "Amazon ECS"
                }
            },
            {
                "name": "Set Up a Data Warehouse",
                "gcloud": {
                    "command": "bq mk --dataset my_project:my_dataset",
                    "service": "BigQuery"
                },
                "azure": {
                    "command": "az synapse workspace create --name my-synapse-workspace --resource-group myResourceGroup --storage-account mystorage --file-system myfilesystem --sql-admin-login-user sqladminuser --sql-admin-login-password Password123!",
                    "service": "Azure Synapse Analytics"
                },
                "aws": {
                    "command": "aws redshift create-cluster --cluster-identifier my-redshift-cluster --node-type dc2.large --number-of-nodes 2 --master-username admin --master-user-password Password123!",
                    "service": "Amazon Redshift"
                }
            },
            {
                "name": "Configure a Content Delivery Network (CDN)",
                "gcloud": {
                    "command": "gcloud compute backend-buckets create my-backend-bucket --gcs-bucket-name my-bucket && gcloud compute url-maps create my-cdn --default-backend-bucket my-backend-bucket",
                    "service": "Cloud CDN"
                },
                "azure": {
                    "command": "az cdn profile create --name my-cdn-profile --resource-group myResourceGroup --sku Standard_Microsoft && az cdn endpoint create --name my-cdn-endpoint --profile-name my-cdn-profile --resource-group myResourceGroup --origin www.example.com",
                    "service": "Azure CDN"
                },
                "aws": {
                    "command": "aws cloudfront create-distribution --origin-domain-name my-bucket.s3.amazonaws.com --default-root-object index.html",
                    "service": "Amazon CloudFront"
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

                service_label = tk.Label(frame, text=f"Service: {details['service']}", font=("Arial", 12, "italic"), bg="black", fg="white")
                service_label.pack(anchor="w")

                command_text = tk.Text(frame, height=4, wrap=tk.WORD, font=("Courier", 12), bg="gray10", fg="white", insertbackground="white")
                command_text.insert(tk.END, details["command"])
                command_text.config(state=tk.DISABLED)
                command_text.pack(fill=tk.X, pady=5)
                command_text.bind("<Double-Button-1>", lambda e, cmd=details["command"]: self.copy_to_clipboard(cmd))

                run_button = tk.Button(frame, text="Run Command", command=lambda cmd=details["command"]: self.run_command(cmd), bg="gray25", fg="white", font=("Arial", 12, "bold"))
                run_button.pack(pady=5)

    def copy_to_clipboard(self, text):
        pyperclip.copy(text)
        print("Command copied to clipboard!")

    def run_command(self, command):
        output_window = tk.Toplevel(self.master)
        output_window.title("Command Output")
        output_window.geometry("800x600")
        output_window.configure(bg="black")

        output_text = tk.Text(output_window, wrap=tk.WORD, font=("Courier", 12), bg="black", fg="white", insertbackground="white")
        output_text.pack(expand=True, fill="both", padx=20, pady=20)

        def execute_command():
            try:
                if platform.system() == "Windows":
                    result = subprocess.run(f"echo Simulating command execution: {command}", shell=True, check=True, capture_output=True, text=True)
                else:
                    result = subprocess.run(f"echo Simulating command execution: {command}", shell=True, check=True, capture_output=True, text=True)
                output = f"Command simulated successfully:\n\n{result.stdout}"
            except subprocess.CalledProcessError as e:
                output = f"Error simulating command:\n\n{e.stderr}"

            output_text.insert(tk.END, output)
            output_text.config(state=tk.DISABLED)

        threading.Thread(target=execute_command).start()

    def open_new_lab(self):
        new_window = tk.Toplevel(self.master)
        new_lab = CloudCLILab(new_window)
        new_lab.tasks = [
            {
                "name": "Set Up a Machine Learning Pipeline",
                "gcloud": {
                    "command": "gcloud ai-platform jobs submit training my_job --region us-central1 --master-image-uri gcr.io/my-project/my-ml-image --scale-tier BASIC",
                    "service": "AI Platform"
                },
                "azure": {
                    "command": "az ml computetarget create amlcompute --name cpu-cluster --vm-size Standard_DS2_v2 --max-nodes 4",
                    "service": "Azure Machine Learning"
                },
                "aws": {
                    "command": "aws sagemaker create-training-job --training-job-name my-training-job --algorithm-specification TrainingImage=12345.dkr.ecr.us-west-2.amazonaws.com/my-algorithm:latest,TrainingInputMode=File",
                    "service": "Amazon SageMaker"
                }
            },
            {
                "name": "Deploy a Containerized Application",
                "gcloud": {
                    "command": "gcloud run deploy --image gcr.io/my-project/my-app:v1 --platform managed",
                    "service": "Cloud Run"
                },
                "azure": {
                    "command": "az container create --resource-group myResourceGroup --name mycontainer --image mycontainerimage:v1 --dns-name-label my-app-label --ports 80",
                    "service": "Azure Container Instances"
                },
                "aws": {
                    "command": "aws ecs run-task --cluster my-cluster --task-definition my-task:1 --count 1 --launch-type FARGATE",
                    "service": "Amazon ECS"
                }
            },
            {
                "name": "Set Up a Logging and Monitoring Solution",
                "gcloud": {
                    "command": "gcloud monitoring dashboards create --config-from-file=dashboard.json",
                    "service": "Cloud Monitoring"
                },
                "azure": {
                    "command": "az monitor log-analytics workspace create --resource-group myResourceGroup --workspace-name my-workspace",
                    "service": "Azure Monitor"
                },
                "aws": {
                    "command": "aws cloudwatch put-dashboard --dashboard-name my-dashboard --dashboard-body file://dashboard.json",
                    "service": "Amazon CloudWatch"
                }
            },
            {
                "name": "Create a Serverless Database",
                "gcloud": {
                    "command": "gcloud firestore databases create --region=us-east1",
                    "service": "Cloud Firestore"
                },
                "azure": {
                    "command": "az cosmosdb create --name my-cosmos-db --resource-group myResourceGroup --kind GlobalDocumentDB",
                    "service": "Azure Cosmos DB"
                },
                "aws": {
                    "command": "aws dynamodb create-table --table-name my-table --attribute-definitions AttributeName=id,AttributeType=S --key-schema AttributeName=id,KeyType=HASH --billing-mode PAY_PER_REQUEST",
                    "service": "Amazon DynamoDB"
                }
            },
            {
                "name": "Set Up a Continuous Integration/Continuous Deployment (CI/CD) Pipeline",
                "gcloud": {
                    "command": "gcloud builds triggers create github --repo-name=my-repo --branch-pattern=main --build-config=cloudbuild.yaml",
                    "service": "Cloud Build"
                },
                "azure": {
                    "command": "az pipelines create --name my-pipeline --repository my-repo --branch main --yml-path azure-pipelines.yml",
                    "service": "Azure Pipelines"
                },
                "aws": {
                    "command": "aws codepipeline create-pipeline --cli-input-json file://pipeline.json",
                    "service": "AWS CodePipeline"
                }
            }
        ]
        new_lab.create_task_tabs()

if __name__ == "__main__":
    root = tk.Tk()
    app = CloudCLILab(root)
    root.mainloop()
