import tkinter as tk
from tkinter import ttk
import subprocess

class CloudCLILab:
    def __init__(self, master):
        self.master = master
        self.master.title("Cloud CLI Lab")
        self.master.geometry("800x600")

        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self.tasks = [
            {
                "name": "Create a Virtual Machine",
                "gcloud": "gcloud compute instances create my-vm --zone=us-central1-a --machine-type=n1-standard-1 --image-family=debian-10 --image-project=debian-cloud",
                "azure": "az vm create --resource-group myResourceGroup --name myVM --image UbuntuLTS --admin-username azureuser --generate-ssh-keys",
                "aws": "aws ec2 run-instances --image-id ami-0c55b159cbfafe1f0 --count 1 --instance-type t2.micro --key-name MyKeyPair --security-group-ids sg-903004f8 --subnet-id subnet-6e7f829e"
            },
            {
                "name": "Create a Storage Bucket/Container",
                "gcloud": "gsutil mb gs://my-unique-bucket-name",
                "azure": "az storage container create --name mycontainer --account-name mystorageaccount",
                "aws": "aws s3 mb s3://my-unique-bucket-name"
            },
            {
                "name": "Deploy a Web App",
                "gcloud": "gcloud app deploy app.yaml",
                "azure": "az webapp up --name mywebapp --html",
                "aws": "aws elasticbeanstalk create-application --application-name mywebapp && aws elasticbeanstalk create-environment --application-name mywebapp --environment-name mywebapp-env --solution-stack-name \"64bit Amazon Linux 2 v5.4.9 running PHP 7.4\""
            },
            {
                "name": "Create a Database Instance",
                "gcloud": "gcloud sql instances create myinstance --tier=db-n1-standard-1 --region=us-central1",
                "azure": "az sql server create --name mysqlserver --resource-group myResourceGroup --location eastus --admin-user azureuser --admin-password ComplexPassword123!",
                "aws": "aws rds create-db-instance --db-instance-identifier mydbinstance --db-instance-class db.t3.micro --engine mysql --master-username admin --master-user-password password123"
            },
            {
                "name": "Set up a Load Balancer",
                "gcloud": "gcloud compute http-health-checks create http-basic-check && gcloud compute target-pools create my-target-pool --region us-central1 --http-health-check http-basic-check && gcloud compute forwarding-rules create my-forwarding-rule --region us-central1 --ports 80 --target-pool my-target-pool",
                "azure": "az network lb create --resource-group myResourceGroup --name myLoadBalancer --sku Standard --public-ip-address myPublicIP && az network lb probe create --resource-group myResourceGroup --lb-name myLoadBalancer --name myHealthProbe --protocol tcp --port 80 && az network lb rule create --resource-group myResourceGroup --lb-name myLoadBalancer --name myLoadBalancerRule --protocol tcp --frontend-port 80 --backend-port 80 --frontend-ip-name LoadBalancerFrontEnd --backend-pool-name myBackEndPool --probe-name myHealthProbe",
                "aws": "aws elbv2 create-load-balancer --name my-load-balancer --subnets subnet-12345678 subnet-87654321 --security-groups sg-12345678 && aws elbv2 create-target-group --name my-targets --protocol HTTP --port 80 --vpc-id vpc-12345678 && aws elbv2 create-listener --load-balancer-arn arn:aws:elasticloadbalancing:us-west-2:123456789012:loadbalancer/app/my-load-balancer/50dc6c495c0c9188 --protocol HTTP --port 80 --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:us-west-2:123456789012:targetgroup/my-targets/73e2d6bc24d8a067"
            }
        ]

        self.create_task_tabs()

        self.finish_button = tk.Button(self.master, text="Finish", command=self.open_new_lab)
        self.finish_button.pack(pady=10)

    def create_task_tabs(self):
        for task in self.tasks:
            tab = ttk.Frame(self.notebook)
            self.notebook.add(tab, text=task["name"])

            gcloud_label = tk.Label(tab, text="Google Cloud (gcloud):", font=("Arial", 12, "bold"))
            gcloud_label.pack(anchor="w", padx=10, pady=5)
            gcloud_text = tk.Text(tab, height=4, wrap=tk.WORD)
            gcloud_text.insert(tk.END, task["gcloud"])
            gcloud_text.config(state=tk.DISABLED)
            gcloud_text.pack(fill=tk.X, padx=10, pady=5)

            azure_label = tk.Label(tab, text="Azure:", font=("Arial", 12, "bold"))
            azure_label.pack(anchor="w", padx=10, pady=5)
            azure_text = tk.Text(tab, height=4, wrap=tk.WORD)
            azure_text.insert(tk.END, task["azure"])
            azure_text.config(state=tk.DISABLED)
            azure_text.pack(fill=tk.X, padx=10, pady=5)

            aws_label = tk.Label(tab, text="AWS:", font=("Arial", 12, "bold"))
            aws_label.pack(anchor="w", padx=10, pady=5)
            aws_text = tk.Text(tab, height=4, wrap=tk.WORD)
            aws_text.insert(tk.END, task["aws"])
            aws_text.config(state=tk.DISABLED)
            aws_text.pack(fill=tk.X, padx=10, pady=5)

            run_button = tk.Button(tab, text="Run Command", command=lambda cmd=task: self.run_command(cmd))
            run_button.pack(pady=10)

    def run_command(self, task):
        cloud_provider = self.get_selected_cloud_provider()
        command = task[cloud_provider]
        try:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            output = result.stdout
        except subprocess.CalledProcessError as e:
            output = f"Error: {e.stderr}"

        output_window = tk.Toplevel(self.master)
        output_window.title("Command Output")
        output_window.geometry("600x400")

        output_text = tk.Text(output_window, wrap=tk.WORD)
        output_text.insert(tk.END, output)
        output_text.config(state=tk.DISABLED)
        output_text.pack(expand=True, fill="both", padx=10, pady=10)

    def get_selected_cloud_provider(self):
        selected_tab = self.notebook.index(self.notebook.select())
        if selected_tab % 3 == 0:
            return "gcloud"
        elif selected_tab % 3 == 1:
            return "azure"
        else:
            return "aws"

    def open_new_lab(self):
        new_window = tk.Toplevel(self.master)
        new_lab = CloudCLILab(new_window)
        new_lab.tasks = [
            {
                "name": "Create a Kubernetes Cluster",
                "gcloud": "gcloud container clusters create my-cluster --zone us-central1-a --num-nodes 3",
                "azure": "az aks create --resource-group myResourceGroup --name myAKSCluster --node-count 3 --enable-addons monitoring --generate-ssh-keys",
                "aws": "eksctl create cluster --name my-cluster --region us-west-2 --nodes 3"
            },
            {
                "name": "Set up a VPN",
                "gcloud": "gcloud compute target-vpn-gateways create my-vpn-gateway --region us-central1 --network default && gcloud compute forwarding-rules create my-fr-esp --region us-central1 --ip-protocol ESP --target-vpn-gateway my-vpn-gateway && gcloud compute forwarding-rules create my-fr-udp500 --region us-central1 --ip-protocol UDP --ports 500 --target-vpn-gateway my-vpn-gateway && gcloud compute forwarding-rules create my-fr-udp4500 --region us-central1 --ip-protocol UDP --ports 4500 --target-vpn-gateway my-vpn-gateway",
                "azure": "az network vnet-gateway create --name myVNetGateway --location eastus --resource-group myResourceGroup --vnet myVNet --public-ip-address myGatewayIP --sku VpnGw1 --gateway-type Vpn --vpn-type RouteBased --no-wait",
                "aws": "aws ec2 create-vpn-gateway --type ipsec.1 && aws ec2 attach-vpn-gateway --vpn-gateway-id vgw-12345678 --vpc-id vpc-12345678 && aws ec2 create-customer-gateway --type ipsec.1 --public-ip 203.0.113.1 --bgp-asn 65000"
            },
            {
                "name": "Deploy a Serverless Function",
                "gcloud": "gcloud functions deploy my-function --runtime python38 --trigger-http --entry-point hello_world",
                "azure": "az functionapp create --resource-group myResourceGroup --consumption-plan-location eastus --runtime python --runtime-version 3.8 --functions-version 3 --name my-function-app --storage-account mystorageaccount",
                "aws": "aws lambda create-function --function-name my-function --runtime python3.8 --role arn:aws:iam::123456789012:role/lambda-role --handler lambda_function.lambda_handler --zip-file fileb://function.zip"
            },
            {
                "name": "Set up Monitoring and Logging",
                "gcloud": "gcloud monitoring dashboards create --config-from-file=dashboard.json",
                "azure": "az monitor log-analytics workspace create --resource-group myResourceGroup --workspace-name myWorkspace",
                "aws": "aws cloudwatch put-dashboard --dashboard-name my-dashboard --dashboard-body file://dashboard.json"
            },
            {
                "name": "Create a Content Delivery Network (CDN)",
                "gcloud": "gcloud compute backend-buckets create my-backend-bucket --gcs-bucket-name my-bucket && gcloud compute url-maps create my-url-map --default-backend-bucket my-backend-bucket && gcloud compute target-http-proxies create my-http-proxy --url-map my-url-map && gcloud compute forwarding-rules create my-forwarding-rule --global --target-http-proxy my-http-proxy --ports 80",
                "azure": "az cdn profile create --resource-group myResourceGroup --name myCDNProfile --sku Standard_Microsoft && az cdn endpoint create --resource-group myResourceGroup --profile-name myCDNProfile --name myCDNEndpoint --origin www.contoso.com",
                "aws": "aws cloudfront create-distribution --origin-domain-name my-bucket.s3.amazonaws.com --default-root-object index.html"
            }
        ]
        new_lab.create_task_tabs()

if __name__ == "__main__":
    root = tk.Tk()
    app = CloudCLILab(root)
    root.mainloop()