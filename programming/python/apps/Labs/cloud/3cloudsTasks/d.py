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
                "name": "Deploy a Microservices Application",
                "gcloud": {
                    "command": "gcloud run deploy microservice-1 --image gcr.io/my-project/microservice-1:v1 --platform managed --region us-central1",
                    "service": "Cloud Run",
                    "output": "Deploying container to Cloud Run service [microservice-1] in project [my-project] region [us-central1]\n"
                             "✓ Deploying... Done.\n"
                             "  ✓ Creating Revision...\n"
                             "  ✓ Routing traffic...\n"
                             "Done.\n"
                             "Service [microservice-1] revision [microservice-1-00001-qwe] has been deployed and is serving 100 percent of traffic.\n"
                             "Service URL: https://microservice-1-a1b2c3d4e5-uc.a.run.app"
                },
                "azure": {
                    "command": "az container create --resource-group myResourceGroup --name microservice-1 --image myacr.azurecr.io/microservice-1:v1 --dns-name-label microservice-1-dns --ports 80",
                    "service": "Azure Container Instances",
                    "output": "{\n"
                             "  \"id\": \"/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myResourceGroup/providers/Microsoft.ContainerInstance/containerGroups/microservice-1\",\n"
                             "  \"name\": \"microservice-1\",\n"
                             "  \"provisioningState\": \"Succeeded\",\n"
                             "  \"fqdn\": \"microservice-1-dns.eastus.azurecontainer.io\",\n"
                             "  \"ipAddress\": {\n"
                             "    \"ip\": \"20.62.198.125\",\n"
                             "    \"ports\": [\n"
                             "      {\n"
                             "        \"port\": 80,\n"
                             "        \"protocol\": \"TCP\"\n"
                             "      }\n"
                             "    ]\n"
                             "  }\n"
                             "}"
                },
                "aws": {
                    "command": "aws ecs create-service --cluster my-cluster --service-name microservice-1 --task-definition microservice-1:1 --desired-count 2 --launch-type FARGATE --network-configuration \"awsvpcConfiguration={subnets=[subnet-12345678,subnet-87654321],securityGroups=[sg-12345a]}\"",
                    "service": "Amazon ECS",
                    "output": "{\n"
                             "    \"service\": {\n"
                             "        \"serviceArn\": \"arn:aws:ecs:us-west-2:123456789012:service/my-cluster/microservice-1\",\n"
                             "        \"serviceName\": \"microservice-1\",\n"
                             "        \"clusterArn\": \"arn:aws:ecs:us-west-2:123456789012:cluster/my-cluster\",\n"
                             "        \"taskDefinition\": \"arn:aws:ecs:us-west-2:123456789012:task-definition/microservice-1:1\",\n"
                             "        \"desiredCount\": 2,\n"
                             "        \"launchType\": \"FARGATE\",\n"
                             "        \"platformVersion\": \"LATEST\",\n"
                             "        \"status\": \"ACTIVE\",\n"
                             "        \"createdAt\": 1623456789.0,\n"
                             "        \"updatedAt\": 1623456789.0\n"
                             "    }\n"
                             "}"
                }
            },
            {
                "name": "Set Up a Serverless Data Pipeline",
                "gcloud": {
                    "command": "gcloud dataflow jobs run my-pipeline --gcs-location gs://dataflow-templates/latest/Word_Count --region us-central1 --staging-location gs://my-bucket/temp",
                    "service": "Cloud Dataflow",
                    "output": "Job ID: 2023-06-15_08_15_16-12345678901234567\n"
                             "Job Name: my-pipeline\n"
                             "Project ID: my-project-id\n"
                             "Region: us-central1\n"
                             "Status: JOB_STATE_RUNNING\n"
                             "The job is currently running. You can check its status using 'gcloud dataflow jobs show 2023-06-15_08_15_16-12345678901234567 --region us-central1'"
                },
                "azure": {
                    "command": "az datafactory pipeline create --factory-name myDataFactory --resource-group myResourceGroup --pipeline-name myPipeline --pipeline @pipeline.json",
                    "service": "Azure Data Factory",
                    "output": "{\n"
                             "  \"id\": \"/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myResourceGroup/providers/Microsoft.DataFactory/factories/myDataFactory/pipelines/myPipeline\",\n"
                             "  \"name\": \"myPipeline\",\n"
                             "  \"type\": \"Microsoft.DataFactory/factories/pipelines\",\n"
                             "  \"properties\": {\n"
                             "    \"activities\": [],\n"
                             "    \"parameters\": {}\n"
                             "  }\n"
                             "}"
                },
                "aws": {
                    "command": "aws glue create-job --name my-etl-job --role AWSGlueServiceRole-DefaultRole --command '{\"Name\":\"glueetl\",\"ScriptLocation\":\"s3://my-bucket/scripts/etl_job.py\"}' --default-arguments '{\"--job-language\":\"python\"}' --max-retries 3",
                    "service": "AWS Glue",
                    "output": "{\n"
                             "    \"Name\": \"my-etl-job\",\n"
                             "    \"Description\": \"\",\n"
                             "    \"Role\": \"AWSGlueServiceRole-DefaultRole\",\n"
                             "    \"ExecutionProperty\": {\n"
                             "        \"MaxConcurrentRuns\": 1\n"
                             "    },\n"
                             "    \"Command\": {\n"
                             "        \"Name\": \"glueetl\",\n"
                             "        \"ScriptLocation\": \"s3://my-bucket/scripts/etl_job.py\"\n"
                             "    },\n"
                             "    \"DefaultArguments\": {\n"
                             "        \"--job-language\": \"python\"\n"
                             "    },\n"
                             "    \"MaxRetries\": 3,\n"
                             "    \"AllocatedCapacity\": 10,\n"
                             "    \"Timeout\": 2880,\n"
                             "    \"MaxCapacity\": 10.0,\n"
                             "    \"WorkerType\": \"G.1X\",\n"
                             "    \"NumberOfWorkers\": 10,\n"
                             "    \"GlueVersion\": \"3.0\"\n"
                             "}"
                }
            },
            {
                "name": "Create a Managed Kubernetes Cluster",
                "gcloud": {
                    "command": "gcloud container clusters create my-cluster --zone us-central1-a --num-nodes 3 --enable-autoscaling --min-nodes 1 --max-nodes 5",
                    "service": "Google Kubernetes Engine (GKE)",
                    "output": "Creating cluster my-cluster in us-central1-a... Cluster is being health-checked...\n"
                             "Created [https://container.googleapis.com/v1/projects/my-project/zones/us-central1-a/clusters/my-cluster].\n"
                             "kubeconfig entry generated for my-cluster.\n"
                             "NAME        LOCATION       MASTER_VERSION  MASTER_IP       MACHINE_TYPE  NODE_VERSION   NUM_NODES  STATUS\n"
                             "my-cluster  us-central1-a  1.21.5-gke.1500  35.184.135.69  e2-medium     1.21.5-gke.1500  3          RUNNING"
                },
                "azure": {
                    "command": "az aks create --resource-group myResourceGroup --name myAKSCluster --node-count 3 --enable-addons monitoring --generate-ssh-keys",
                    "service": "Azure Kubernetes Service (AKS)",
                    "output": "{\n"
                             "  \"id\": \"/subscriptions/12345678-1234-1234-1234-123456789012/resourcegroups/myResourceGroup/providers/Microsoft.ContainerService/managedClusters/myAKSCluster\",\n"
                             "  \"location\": \"eastus\",\n"
                             "  \"name\": \"myAKSCluster\",\n"
                             "  \"provisioningState\": \"Succeeded\",\n"
                             "  \"kubernetesVersion\": \"1.21.7\",\n"
                             "  \"nodeResourceGroup\": \"MC_myResourceGroup_myAKSCluster_eastus\",\n"
                             "  \"enableRBAC\": true,\n"
                             "  \"fqdn\": \"myaksclust-myresourcegroup-12345-12345.hcp.eastus.azmk8s.io\"\n"
                             "}"
                },
                "aws": {
                    "command": "eksctl create cluster --name my-cluster --region us-west-2 --nodegroup-name standard-workers --node-type t3.medium --nodes 3 --nodes-min 1 --nodes-max 5 --managed",
                    "service": "Amazon Elastic Kubernetes Service (EKS)",
                    "output": "[✓]  EKS cluster \"my-cluster\" in \"us-west-2\" region is ready\n"
                             "[✓]  created serviceaccount \"eks-pod-identity-agent\" in kube-system namespace\n"
                             "[✓]  daemonset \"eks-pod-identity-agent\" created\n"
                             "[✓]  added 3 nodes \"ip-192-168-12-34.us-west-2.compute.internal\" to cluster \"my-cluster\"\n"
                             "[✓]  nodegroup \"standard-workers\" has 3 node(s)\n"
                             "[✓]  node \"ip-192-168-12-34.us-west-2.compute.internal\" is ready\n"
                             "[✓]  kubectl command should work with \"/home/user/.kube/config\", try 'kubectl get nodes'\n"
                             "[✓]  EKS cluster \"my-cluster\" in \"us-west-2\" region is ready"
                }
            },
            {
                "name": "Set Up a Globally Distributed Database",
                "gcloud": {
                    "command": "gcloud spanner instances create my-instance --config=regional-us-central1 --description=\"My Spanner Instance\" --nodes=3",
                    "service": "Cloud Spanner",
                    "output": "Creating instance...done.\n"
                             "Created instance [my-instance].\n"
                             "Instance ID: my-instance\n"
                             "Display Name: My Spanner Instance\n"
                             "Node count: 3\n"
                             "Config: regional-us-central1\n"
                             "State: READY"
                },
                "azure": {
                    "command": "az cosmosdb create --name myCosmosAccount --resource-group myResourceGroup --kind GlobalDocumentDB --locations regionName=eastus failoverPriority=0 isZoneRedundant=False",
                    "service": "Azure Cosmos DB",
                    "output": "{\n"
                             "  \"consistencyPolicy\": {\n"
                             "    \"defaultConsistencyLevel\": \"Session\"\n"
                             "  },\n"
                             "  \"databaseAccountOfferType\": \"Standard\",\n"
                             "  \"documentEndpoint\": \"https://mycosmosaccount.documents.azure.com:443/\",\n"
                             "  \"enableAutomaticFailover\": false,\n"
                             "  \"enableMultipleWriteLocations\": false,\n"
                             "  \"id\": \"/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myResourceGroup/providers/Microsoft.DocumentDB/databaseAccounts/myCosmosAccount\",\n"
                             "  \"kind\": \"GlobalDocumentDB\",\n"
                             "  \"location\": \"East US\",\n"
                             "  \"locations\": [\n"
                             "    {\n"
                             "      \"failoverPriority\": 0,\n"
                             "      \"isZoneRedundant\": false,\n"
                             "      \"locationName\": \"East US\"\n"
                             "    }\n"
                             "  ],\n"
                             "  \"name\": \"myCosmosAccount\",\n"
                             "  \"provisioningState\": \"Succeeded\",\n"
                             "  \"readLocations\": [\n"
                             "    {\n"
                             "      \"documentEndpoint\": \"https://mycosmosaccount-eastus.documents.azure.com:443/\",\n"
                             "      \"failoverPriority\": 0,\n"
                             "      \"id\": \"myCosmosAccount-eastus\",\n"
                             "      \"locationName\": \"East US\",\n"
                             "      \"provisioningState\": \"Succeeded\"\n"
                             "    }\n"
                             "  ],\n"
                             "  \"writeLocations\": [\n"
                             "    {\n"
                             "      \"documentEndpoint\": \"https://mycosmosaccount-eastus.documents.azure.com:443/\",\n"
                             "      \"failoverPriority\": 0,\n"
                             "      \"id\": \"myCosmosAccount-eastus\",\n"
                             "      \"locationName\": \"East US\",\n"
"      \"provisioningState\": \"Succeeded\"\n"
                             "    }\n"
                             "  ]\n"
                             "}"
                },
                "aws": {
                    "command": "aws dynamodb create-global-table --global-table-name my-global-table --replication-group RegionName=us-east-1 RegionName=eu-west-1 RegionName=ap-northeast-1",
                    "service": "Amazon DynamoDB",
                    "output": "{\n"
                             "    \"GlobalTableDescription\": {\n"
                             "        \"GlobalTableName\": \"my-global-table\",\n"
                             "        \"GlobalTableStatus\": \"CREATING\",\n"
                             "        \"ReplicationGroup\": [\n"
                             "            {\n"
                             "                \"RegionName\": \"us-east-1\"\n"
                             "            },\n"
                             "            {\n"
                             "                \"RegionName\": \"eu-west-1\"\n"
                             "            },\n"
                             "            {\n"
                             "                \"RegionName\": \"ap-northeast-1\"\n"
                             "            }\n"
                             "        ]\n"
                             "    }\n"
                             "}"
                }
            },
            {
                "name": "Deploy a Scalable Machine Learning Model",
                "gcloud": {
                    "command": "gcloud ai-platform models create my_model --regions us-central1 && gcloud ai-platform versions create v1 --model my_model --origin gs://my-bucket/model --runtime-version 2.5 --framework tensorflow --python-version 3.7",
                    "service": "AI Platform",
                    "output": "Created model [my_model].\n"
                             "Creating version (this might take a few minutes)......done.\n"
                             "Creating Version...done.\n\n"
                             "name: projects/my-project/models/my_model/versions/v1\n"
                             "createTime: '2023-06-15T10:30:00Z'\n"
                             "deploymentUri: gs://my-bucket/model\n"
                             "framework: TENSORFLOW\n"
                             "machineType: mls1-c1-m2\n"
                             "pythonVersion: '3.7'\n"
                             "runtimeVersion: '2.5'\n"
                             "state: READY"
                },
                "azure": {
                    "command": "az ml model deploy --name my-model-service --model my-model:1 --inference-config-file inference-config.yml --deploy-config-file deployment-config.yml --workspace-name my-workspace --resource-group myResourceGroup",
                    "service": "Azure Machine Learning",
                    "output": "{\n"
                             "  \"computeType\": \"AKS\",\n"
                             "  \"location\": \"eastus\",\n"
                             "  \"modelId\": \"/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myResourceGroup/providers/Microsoft.MachineLearningServices/workspaces/my-workspace/models/my-model/versions/1\",\n"
                             "  \"name\": \"my-model-service\",\n"
                             "  \"provisioningState\": \"Succeeded\",\n"
                             "  \"scoringUri\": \"http://4a1b2c3d4e5f.eastus.azurecontainer.io/score\",\n"
                             "  \"state\": \"Healthy\",\n"
                             "  \"tags\": {},\n"
                             "  \"type\": \"Microsoft.MachineLearningServices/workspaces/deployments\"\n"
                             "}"
                },
                "aws": {
                    "command": "aws sagemaker create-model --model-name my-model --primary-container '{\"Image\":\"1234567890.dkr.ecr.us-west-2.amazonaws.com/my-algorithm:latest\",\"ModelDataUrl\":\"s3://my-bucket/model.tar.gz\"}' --execution-role-arn arn:aws:iam::123456789012:role/SageMakerRole",
                    "service": "Amazon SageMaker",
                    "output": "{\n"
                             "    \"ModelArn\": \"arn:aws:sagemaker:us-west-2:123456789012:model/my-model\"\n"
                             "}\n\n"
                             "aws sagemaker create-endpoint-config --endpoint-config-name my-endpoint-config --production-variants '{\"InstanceType\":\"ml.t2.medium\",\"InitialVariantWeight\":1,\"InitialInstanceCount\":1,\"ModelName\":\"my-model\",\"VariantName\":\"AllTraffic\"}'\n\n"
                             "{\n"
                             "    \"EndpointConfigArn\": \"arn:aws:sagemaker:us-west-2:123456789012:endpoint-config/my-endpoint-config\"\n"
                             "}\n\n"
                             "aws sagemaker create-endpoint --endpoint-name my-endpoint --endpoint-config-name my-endpoint-config\n\n"
                             "{\n"
                             "    \"EndpointArn\": \"arn:aws:sagemaker:us-west-2:123456789012:endpoint/my-endpoint\"\n"
                             "}"
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

                run_button = tk.Button(frame, text="Run Command", command=lambda cmd=details["command"], output=details["output"]: self.run_command(cmd, output), bg="gray25", fg="white", font=("Arial", 12, "bold"))
                run_button.pack(pady=5)

    def copy_to_clipboard(self, text):
        pyperclip.copy(text)
        print("Command copied to clipboard!")

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
