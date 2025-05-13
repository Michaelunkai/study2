import tkinter as tk
from tkinter import ttk
import subprocess
import threading

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
                "name": "Launch a Virtual Machine",
                "gcloud": {
                    "command": "gcloud compute instances create my-vm --zone=us-central1-a --machine-type=n1-standard-1 --image-family=debian-10 --image-project=debian-cloud",
                    "service": "Compute Engine"
                },
                "azure": {
                    "command": "az vm create --resource-group myResourceGroup --name myVM --image UbuntuLTS --admin-username azureuser --generate-ssh-keys",
                    "service": "Azure Virtual Machines"
                },
                "aws": {
                    "command": "aws ec2 run-instances --image-id ami-0c55b159cbfafe1f0 --count 1 --instance-type t2.micro --key-name MyKeyPair --security-group-ids sg-903004f8 --subnet-id subnet-6e7f829e",
                    "service": "Amazon EC2"
                }
            },
            {
                "name": "Create a Cloud Storage Bucket",
                "gcloud": {
                    "command": "gsutil mb gs://my-unique-bucket-name",
                    "service": "Cloud Storage"
                },
                "azure": {
                    "command": "az storage container create --name mycontainer --account-name mystorageaccount",
                    "service": "Azure Blob Storage"
                },
                "aws": {
                    "command": "aws s3 mb s3://my-unique-bucket-name",
                    "service": "Amazon S3"
                }
            },
            {
                "name": "Deploy a Simple Web Application",
                "gcloud": {
                    "command": "gcloud app deploy app.yaml",
                    "service": "App Engine"
                },
                "azure": {
                    "command": "az webapp up --name mywebapp --html",
                    "service": "Azure App Service"
                },
                "aws": {
                    "command": "aws elasticbeanstalk create-application --application-name mywebapp && aws elasticbeanstalk create-environment --application-name mywebapp --environment-name mywebapp-env --solution-stack-name \"64bit Amazon Linux 2 v5.4.9 running PHP 7.4\"",
                    "service": "AWS Elastic Beanstalk"
                }
            },
            {
                "name": "Set Up a Cloud Database",
                "gcloud": {
                    "command": "gcloud sql instances create myinstance --tier=db-n1-standard-1 --region=us-central1",
                    "service": "Cloud SQL"
                },
                "azure": {
                    "command": "az sql server create --name mysqlserver --resource-group myResourceGroup --location eastus --admin-user azureuser --admin-password ComplexPassword123!",
                    "service": "Azure SQL Database"
                },
                "aws": {
                    "command": "aws rds create-db-instance --db-instance-identifier mydbinstance --db-instance-class db.t3.micro --engine mysql --master-username admin --master-user-password password123",
                    "service": "Amazon RDS"
                }
            },
            {
                "name": "Configure a Load Balancer",
                "gcloud": {
                    "command": "gcloud compute http-health-checks create http-basic-check && gcloud compute target-pools create my-target-pool --region us-central1 --http-health-check http-basic-check && gcloud compute forwarding-rules create my-forwarding-rule --region us-central1 --ports 80 --target-pool my-target-pool",
                    "service": "Cloud Load Balancing"
                },
                "azure": {
                    "command": "az network lb create --resource-group myResourceGroup --name myLoadBalancer --sku Standard --public-ip-address myPublicIP && az network lb probe create --resource-group myResourceGroup --lb-name myLoadBalancer --name myHealthProbe --protocol tcp --port 80 && az network lb rule create --resource-group myResourceGroup --lb-name myLoadBalancer --name myLoadBalancerRule --protocol tcp --frontend-port 80 --backend-port 80 --frontend-ip-name LoadBalancerFrontEnd --backend-pool-name myBackEndPool --probe-name myHealthProbe",
                    "service": "Azure Load Balancer"
                },
                "aws": {
                    "command": "aws elbv2 create-load-balancer --name my-load-balancer --subnets subnet-12345678 subnet-87654321 --security-groups sg-12345678 && aws elbv2 create-target-group --name my-targets --protocol HTTP --port 80 --vpc-id vpc-12345678 && aws elbv2 create-listener --load-balancer-arn arn:aws:elasticloadbalancing:us-west-2:123456789012:loadbalancer/app/my-load-balancer/50dc6c495c0c9188 --protocol HTTP --port 80 --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:us-west-2:123456789012:targetgroup/my-targets/73e2d6bc24d8a067",
                    "service": "Elastic Load Balancing"
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

                run_button = tk.Button(frame, text="Run Command", command=lambda cmd=details["command"]: self.run_command(cmd), bg="gray25", fg="white", font=("Arial", 12, "bold"))
                run_button.pack(pady=5)

    def run_command(self, command):
        output_window = tk.Toplevel(self.master)
        output_window.title("Command Output")
        output_window.geometry("800x600")
        output_window.configure(bg="black")

        output_text = tk.Text(output_window, wrap=tk.WORD, font=("Courier", 12), bg="black", fg="white", insertbackground="white")
        output_text.pack(expand=True, fill="both", padx=20, pady=20)

        def execute_command():
            try:
                result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
                output = f"Command executed successfully:\n\n{result.stdout}"
            except subprocess.CalledProcessError as e:
                output = f"Error executing command:\n\n{e.stderr}"

            output_text.insert(tk.END, output)
            output_text.config(state=tk.DISABLED)

        threading.Thread(target=execute_command).start()

    def open_new_lab(self):
        new_window = tk.Toplevel(self.master)
        new_lab = CloudCLILab(new_window)
        new_lab.tasks = [
            {
                "name": "Create a Kubernetes Cluster",
                "gcloud": {
                    "command": "gcloud container clusters create my-cluster --zone us-central1-a --num-nodes 3",
                    "service": "Google Kubernetes Engine (GKE)"
                },
                "azure": {
                    "command": "az aks create --resource-group myResourceGroup --name myAKSCluster --node-count 3 --enable-addons monitoring --generate-ssh-keys",
                    "service": "Azure Kubernetes Service (AKS)"
                },
                "aws": {
                    "command": "eksctl create cluster --name my-cluster --region us-west-2 --nodes 3",
                    "service": "Amazon Elastic Kubernetes Service (EKS)"
                }
            },
            {
                "name": "Set up a Virtual Private Network (VPN)",
                "gcloud": {
                    "command": "gcloud compute target-vpn-gateways create my-vpn-gateway --region us-central1 --network default && gcloud compute forwarding-rules create my-fr-esp --region us-central1 --ip-protocol ESP --target-vpn-gateway my-vpn-gateway && gcloud compute forwarding-rules create my-fr-udp500 --region us-central1 --ip-protocol UDP --ports 500 --target-vpn-gateway my-vpn-gateway",
                    "service": "Cloud VPN"
                },
                "azure": {
                    "command": "az network vnet-gateway create --name myVNetGateway --location eastus --resource-group myResourceGroup --vnet myVNet --public-ip-address myGatewayIP --sku VpnGw1 --gateway-type Vpn --vpn-type RouteBased --no-wait",
                    "service": "Azure VPN Gateway"
                },
                "aws": {
                    "command": "aws ec2 create-vpn-gateway --type ipsec.1 && aws ec2 attach-vpn-gateway --vpn-gateway-id vgw-12345678 --vpc-id vpc-12345678 && aws ec2 create-customer-gateway --type ipsec.1 --public-ip 203.0.113.1 --bgp-asn 65000",
                    "service": "AWS VPN"
                }
            },
            {
                "name": "Deploy a Serverless Function",
                "gcloud": {
                    "command": "gcloud functions deploy my-function --runtime python38 --trigger-http --entry-point hello_world",
                    "service": "Cloud Functions"
                },
                "azure": {
                    "command": "az functionapp create --resource-group myResourceGroup --consumption-plan-location eastus --runtime python --runtime-version 3.8 --functions-version 3 --name my-function-app --storage-account mystorageaccount",
                    "service": "Azure Functions"
                },
                "aws": {
                    "command": "aws lambda create-function --function-name my-function --runtime python3.8 --role arn:aws:iam::123456789012:role/lambda-role --handler lambda_function.lambda_handler --zip-file fileb://function.zip",
                    "service": "AWS Lambda"
                }
            },
            {
                "name": "Set up Monitoring and Logging",
                "gcloud": {
                    "command": "gcloud monitoring dashboards create --config-from-file=dashboard.json",
                    "service": "Cloud Monitoring"
                },
                "azure": {
                    "command": "az monitor log-analytics workspace create --resource-group myResourceGroup --workspace-name myWorkspace",
                    "service": "Azure Monitor"
                },
                "aws": {
                    "command": "aws cloudwatch put-dashboard --dashboard-name my-dashboard --dashboard-body file://dashboard.json",
                    "service": "Amazon CloudWatch"
                }
            },
            {
                "name": "Create a Content Delivery Network (CDN)",
                "gcloud": {
                    "command": "gcloud compute backend-buckets create my-backend-bucket --gcs-bucket-name my-bucket && gcloud compute url-maps create my-url-map --default-backend-bucket my-backend-bucket && gcloud compute target-http-proxies create my-http-proxy --url-map my-url-map && gcloud compute forwarding-rules create my-forwarding-rule --global --target-http-proxy my-http-proxy --ports 80",
                    "service": "Cloud CDN"
                },
                "azure": {
                    "command": "az cdn profile create --resource-group myResourceGroup --name myCDNProfile --sku Standard_Microsoft && az cdn endpoint create --resource-group myResourceGroup --profile-name myCDNProfile --name myCDNEndpoint --origin www.contoso.com",
                    "service": "Azure CDN"
                },
                "aws": {
                    "command": "aws cloudfront create-distribution --origin-domain-name my-bucket.s3.amazonaws.com --default-root-object index.html",
                    "service": "Amazon CloudFront"
                }
            }
        ]
        new_lab.create_task_tabs()

if __name__ == "__main__":
    root = tk.Tk()
    app = CloudCLILab(root)
    root.mainloop()