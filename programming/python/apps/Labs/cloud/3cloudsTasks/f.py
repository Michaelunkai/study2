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
                "name": "Create a Kubernetes Cluster",
                "gcloud": {
                    "command": "gcloud container clusters create my-cluster --zone us-central1-a --num-nodes 3",
                    "service": "Google Kubernetes Engine",
                    "output": "Creating cluster...done.\nCluster [my-cluster] created in [us-central1-a].\nNodes: 3\nStatus: RUNNING"
                },
                "azure": {
                    "command": "az aks create --resource-group myResourceGroup --name myAKSCluster --node-count 3 --enable-addons monitoring --generate-ssh-keys",
                    "service": "Azure Kubernetes Service",
                    "output": "Created AKS cluster [myAKSCluster] in resource group [myResourceGroup].\nNode count: 3\nStatus: Succeeded"
                },
                "aws": {
                    "command": "aws eks create-cluster --name my-cluster --role-arn arn:aws:iam::123456789012:role/EKS-Cluster-Role --resources-vpc-config subnetIds=subnet-12345678,subnet-87654321",
                    "service": "Amazon EKS",
                    "output": "Creating EKS cluster...\nCluster ARN: arn:aws:eks:us-west-2:123456789012:cluster/my-cluster\nStatus: CREATING"
                }
            },
            {
                "name": "Deploy a Docker Image to a Container Registry",
                "gcloud": {
                    "command": "gcloud builds submit --tag gcr.io/my-project/my-image",
                    "service": "Google Container Registry",
                    "output": "Submitting build...done.\nImage [gcr.io/my-project/my-image] created successfully."
                },
                "azure": {
                    "command": "az acr build --registry myRegistry --image my-image:latest .",
                    "service": "Azure Container Registry",
                    "output": "Building image...\nImage [my-image:latest] pushed to [myRegistry].\nStatus: Succeeded"
                },
                "aws": {
                    "command": "aws ecr create-repository --repository-name my-repo && docker tag my-image:latest 123456789012.dkr.ecr.us-west-2.amazonaws.com/my-repo:latest && docker push 123456789012.dkr.ecr.us-west-2.amazonaws.com/my-repo:latest",
                    "service": "Amazon ECR",
                    "output": "Creating repository [my-repo]...\nTagging and pushing image...\nImage [my-repo:latest] pushed to ECR."
                }
            },
            {
                "name": "Configure a Load Balancer",
                "gcloud": {
                    "command": "gcloud compute forwarding-rules create my-load-balancer --region us-central1 --ports 80 --target-http-proxy my-proxy --global",
                    "service": "Google Cloud Load Balancing",
                    "output": "Creating forwarding rule...done.\nForwarding rule [my-load-balancer] created.\nRegion: us-central1\nPorts: 80"
                },
                "azure": {
                    "command": "az network lb create --resource-group myResourceGroup --name myLoadBalancer --sku Standard --frontend-ip-name myFrontEnd --backend-pool-name myBackEndPool --public-ip-address myPublicIP",
                    "service": "Azure Load Balancer",
                    "output": "Created load balancer [myLoadBalancer] in resource group [myResourceGroup].\nSKU: Standard\nFrontend IP: myPublicIP"
                },
                "aws": {
                    "command": "aws elb create-load-balancer --load-balancer-name my-load-balancer --listeners Protocol=HTTP,LoadBalancerPort=80,InstanceProtocol=HTTP,InstancePort=80 --availability-zones us-west-2a",
                    "service": "Amazon ELB",
                    "output": "Creating load balancer...\nLoad balancer [my-load-balancer] created.\nListeners: HTTP:80\nAvailability Zones: us-west-2a"
                }
            },
            {
                "name": "Set Up a Message Queue",
                "gcloud": {
                    "command": "gcloud pubsub topics create my-topic",
                    "service": "Google Cloud Pub/Sub",
                    "output": "Creating topic...done.\nTopic [my-topic] created."
                },
                "azure": {
                    "command": "az servicebus topic create --resource-group myResourceGroup --namespace-name myNamespace --name myTopic",
                    "service": "Azure Service Bus",
                    "output": "Created Service Bus topic [myTopic] in namespace [myNamespace]."
                },
                "aws": {
                    "command": "aws sqs create-queue --queue-name my-queue",
                    "service": "Amazon SQS",
                    "output": "Creating SQS queue...\nQueue URL: https://sqs.us-west-2.amazonaws.com/123456789012/my-queue"
                }
            },
            {
                "name": "Create and Configure a CDN",
                "gcloud": {
                    "command": "gcloud compute url-maps create my-map --default-service my-backend-service && gcloud compute target-http-proxies create my-proxy --url-map my-map && gcloud compute forwarding-rules create my-rule --global --target-http-proxy my-proxy --ports 80",
                    "service": "Google Cloud CDN",
                    "output": "Creating URL map...done.\nCreating target HTTP proxy...done.\nCreating forwarding rule...done.\nCDN setup complete."
                },
                "azure": {
                    "command": "az cdn profile create --resource-group myResourceGroup --name myCDNProfile --sku Standard_Microsoft && az cdn endpoint create --resource-group myResourceGroup --profile-name myCDNProfile --name myEndpoint --origin myorigin.example.com",
                    "service": "Azure CDN",
                    "output": "Created CDN profile [myCDNProfile].\nCreated CDN endpoint [myEndpoint]."
                },
                "aws": {
                    "command": "aws cloudfront create-distribution --origin-domain-name mybucket.s3.amazonaws.com --default-root-object index.html",
                    "service": "Amazon CloudFront",
                    "output": "Creating CloudFront distribution...\nDistribution ID: E1234567890ABC\nStatus: Deployed"
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
                cloud_label.bind("<Double-Button-1>", lambda e, task_name=task["name"]: self.copy_task_to_clipboard(task_name))

                service_label = tk.Label(frame, text=f"Service: {details['service']}", font=("Arial", 12, "italic"), bg="black", fg="white")
                service_label.pack(anchor="w")
                service_label.bind("<Double-Button-1>", lambda e, task_name=task["name"]: self.copy_task_to_clipboard(task_name))

                command_text = tk.Text(frame, height=4, wrap=tk.WORD, font=("Courier", 12), bg="gray10", fg="white", insertbackground="white")
                command_text.insert(tk.END, details["command"])
                command_text.config(state=tk.DISABLED)
                command_text.pack(fill=tk.X, pady=5)
                command_text.bind("<Double-Button-1>", lambda e, text=details["command"]: self.copy_to_clipboard(text))

                run_button = tk.Button(frame, text="Run Command", command=lambda cmd=details["command"], output=details["output"]: self.run_command(cmd, output), bg="gray25", fg="white", font=("Arial", 12, "bold"))
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
