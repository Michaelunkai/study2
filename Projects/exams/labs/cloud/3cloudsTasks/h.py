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
        self.master.configure(bg="#1c1c1c")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background="#1c1c1c", borderwidth=0)
        style.configure("TNotebook.Tab", background="#333333", foreground="#cccccc", padding=[10, 5], font=("Arial", 12, "bold"))
        style.map("TNotebook.Tab", background=[("selected", "#00bfff")], foreground=[("selected", "#ffffff")])

        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill="both", padx=20, pady=20)

        self.tasks = [
            {
                "name": "Set Up Kubernetes Monitoring",
                "gcloud": {
                    "command": "kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.2.0/aio/deploy/recommended.yaml",
                    "service": "Kubernetes Dashboard",
                    "output": "Dashboard deployed. Access it using 'kubectl proxy' and visit http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/."
                },
                "azure": {
                    "command": "az aks enable-addons --resource-group myResourceGroup --name myAKSCluster --addons monitoring --workspace-resource-id '/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace>'",
                    "service": "Azure Kubernetes Service Monitoring",
                    "output": "Monitoring enabled for AKS cluster [myAKSCluster]."
                },
                "aws": {
                    "command": "eksctl utils associate-iam-oidc-provider --region us-west-2 --cluster my-cluster --approve && eksctl create iamserviceaccount --name fluentd-cloudwatch --namespace kube-system --cluster my-cluster --attach-policy-arn arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy --approve --override-existing-serviceaccounts",
                    "service": "Amazon EKS Monitoring",
                    "output": "IAM OIDC provider and Fluentd service account associated with EKS cluster [my-cluster]. Monitoring enabled."
                }
            },
            {
                "name": "Deploy a Machine Learning Model",
                "gcloud": {
                    "command": "gcloud ai-platform models create my_model && gcloud ai-platform versions create v1 --model my_model --origin gs://my-bucket/model --runtime-version 2.1 --python-version 3.7",
                    "service": "Google AI Platform",
                    "output": "Model [my_model] created and version [v1] deployed successfully."
                },
                "azure": {
                    "command": "az ml model deploy --name myModel --model my-model:1 --inference-config inferenceConfig.json --deployment-config deploymentConfig.json --resource-group myResourceGroup --workspace-name myWorkspace",
                    "service": "Azure Machine Learning",
                    "output": "Model [myModel] deployed successfully in Azure ML Workspace [myWorkspace]."
                },
                "aws": {
                    "command": "aws sagemaker create-model --model-name my-model --primary-container Image=123456789012.dkr.ecr.us-west-2.amazonaws.com/my-algorithm:latest,ModelDataUrl=s3://my-bucket/model.tar.gz --execution-role-arn arn:aws:iam::123456789012:role/service-role/AmazonSageMaker-ExecutionRole-20200101T000001",
                    "service": "Amazon SageMaker",
                    "output": "Model [my-model] created successfully in SageMaker."
                }
            },
            {
                "name": "Configure a CDN",
                "gcloud": {
                    "command": "gcloud compute backend-buckets create my-backend-bucket --gcs-bucket-name=my-bucket && gcloud compute url-maps create my-url-map --default-backend-bucket=my-backend-bucket && gcloud compute target-http-proxies create http-lb-proxy --url-map=my-url-map && gcloud compute forwarding-rules create http-content-rule --global --target-http-proxy=http-lb-proxy --ports=80",
                    "service": "Google Cloud CDN",
                    "output": "CDN configured successfully with backend bucket [my-backend-bucket]."
                },
                "azure": {
                    "command": "az cdn endpoint create --resource-group myResourceGroup --profile-name myCDNProfile --name myEndpoint --origin myorigin.azureedge.net --no-http --no-https",
                    "service": "Azure CDN",
                    "output": "CDN endpoint [myEndpoint] created successfully in profile [myCDNProfile]."
                },
                "aws": {
                    "command": "aws cloudfront create-distribution --origin-domain-name mybucket.s3.amazonaws.com --default-root-object index.html",
                    "service": "Amazon CloudFront",
                    "output": "CloudFront distribution created successfully with origin [mybucket.s3.amazonaws.com]."
                }
            },
            {
                "name": "Deploy a Multi-Region Database",
                "gcloud": {
                    "command": "gcloud spanner instances create my-instance --config=regional-us-central1 --description='My Spanner Instance' --nodes=3 && gcloud spanner databases create my-database --instance=my-instance --ddl='CREATE TABLE Singers (SingerId INT64 NOT NULL, FirstName STRING(1024), LastName STRING(1024)) PRIMARY KEY(SingerId)'",
                    "service": "Google Cloud Spanner",
                    "output": "Spanner instance [my-instance] and database [my-database] created successfully."
                },
                "azure": {
                    "command": "az cosmosdb create --name myCosmosDB --resource-group myResourceGroup --locations regionName=East US failoverPriority=0 isZoneRedundant=False --kind GlobalDocumentDB && az cosmosdb sql database create --account-name myCosmosDB --resource-group myResourceGroup --name myDatabase",
                    "service": "Azure Cosmos DB",
                    "output": "Cosmos DB [myCosmosDB] and database [myDatabase] created successfully."
                },
                "aws": {
                    "command": "aws dynamodb create-global-table --global-table-name my-global-table --replication-group RegionName=us-east-1 RegionName=eu-west-1",
                    "service": "Amazon DynamoDB",
                    "output": "Global DynamoDB table [my-global-table] created successfully across regions [us-east-1, eu-west-1]."
                }
            },
            {
                "name": "Set Up a CI/CD Pipeline with Security Scans",
                "gcloud": {
                    "command": "gcloud builds submit --tag gcr.io/my-project/my-app && gcloud container images add-tag gcr.io/my-project/my-app gcr.io/my-project/my-app:latest && gcloud beta container analysis notes create --project=my-project --occurrence-filter='resourceUrl=gcr.io/my-project/my-app@sha256:*' --note-id=my-vuln-scan --short-description='Vulnerability scan' --description='A vulnerability scan note for my app'",
                    "service": "Google Cloud Build & Container Analysis",
                    "output": "Build and security scan configured successfully for container [my-app]."
                },
                "azure": {
                    "command": "az pipelines create --name myPipeline --repository myRepo --branch master --yml-path /azure-pipelines.yml && az pipelines variable-group create --name myVarGroup --authorize true --variables MY_VAR=my_value && az security scan create --name myScan --resource-group myResourceGroup --type azuredevops --source-pipeline myPipeline",
                    "service": "Azure Pipelines & Security",
                    "output": "CI/CD pipeline and security scan configured successfully in Azure DevOps."
                },
                "aws": {
                    "command": "aws codepipeline create-pipeline --cli-input-json file://pipeline.json && aws codebuild create-project --name my-scan-project --source type=S3,location=mybucket/build.zip --artifacts type=NO_ARTIFACTS --environment computeType=BUILD_GENERAL1_SMALL,image=aws/codebuild/standard:4.0,privilegedMode=true --service-role arn:aws:iam::123456789012:role/service-role/AWSCodeBuildServiceRole && aws inspector create-assessment-target --assessment-target-name my-target --resource-group-tags key=Name,value=my-app",
                    "service": "AWS CodePipeline & Inspector",
                    "output": "CI/CD pipeline and security scan configured successfully for AWS Inspector."
                }
            }
        ]

        self.create_task_tabs()

        self.finish_button = tk.Button(self.master, text="Finish", command=self.open_new_lab, bg="#00bfff", fg="white", font=("Arial", 14, "bold"))
        self.finish_button.pack(pady=20)

    def create_task_tabs(self):
        for task in self.tasks:
            tab = ttk.Frame(self.notebook, style="TNotebook")
            self.notebook.add(tab, text=task["name"])

            for cloud, details in [("Google Cloud", task["gcloud"]), ("Azure", task["azure"]), ("AWS", task["aws"])]:
                frame = tk.Frame(tab, bg="#1c1c1c")
                frame.pack(fill=tk.X, padx=20, pady=10)

                cloud_label = tk.Label(frame, text=f"{cloud}:", font=("Arial", 16, "bold"), bg="#1c1c1c", fg="#00bfff")
                cloud_label.pack(anchor="w")
                cloud_label.bind("<Double-Button-1>", lambda e, task_name=task["name"]: self.copy_task_to_clipboard(task_name))

                service_label = tk.Label(frame, text=f"Service: {details['service']}", font=("Arial", 12, "italic"), bg="#1c1c1c", fg="#ffffff")
                service_label.pack(anchor="w")
                service_label.bind("<Double-Button-1>", lambda e, task_name=task["name"]: self.copy_task_to_clipboard(task_name))

                command_text = tk.Text(frame, height=4, wrap=tk.WORD, font=("Courier", 12), bg="#333333", fg="#ffffff", insertbackground="white")
                command_text.insert(tk.END, details["command"])
                command_text.config(state=tk.DISABLED)
                command_text.pack(fill=tk.X, pady=5)
                command_text.bind("<Double-Button-1>", lambda e, text=details["command"]: self.copy_to_clipboard(text))

                run_button = tk.Button(frame, text="Run Command", command=lambda cmd=details["command"], output=details["output"]: self.run_command(cmd, output), bg="#00bfff", fg="white", font=("Arial", 12, "bold"))
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
        output_window.configure(bg="#1c1c1c")

        output_text = tk.Text(output_window, wrap=tk.WORD, font=("Courier", 12), bg="#333333", fg="#ffffff", insertbackground="white")
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
