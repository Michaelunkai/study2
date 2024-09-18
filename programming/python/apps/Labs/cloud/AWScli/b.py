import tkinter as tk
from tkinter import ttk, scrolledtext
import random
import pyperclip
import uuid

class AWSCLILab:
    def __init__(self, master):
        self.master = master
        self.master.title("AWS CLI Lab")
        self.master.geometry("1000x800")
        self.master.configure(bg="#2c3e50")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#2c3e50")
        self.style.configure("TLabel", background="#34495e", foreground="#ecf0f1", font=("Arial", 16, "bold"))
        self.style.configure("TButton", background="#3498db", foreground="white", font=("Arial", 10, "bold"), padding=5)
        self.style.map("TButton", background=[("active", "#2980b9")])

        self.services = ["EC2", "S3", "RDS", "Lambda", "ECS"]
        self.current_service = None
        self.unique_id = str(uuid.uuid4())[:8]

        self.create_widgets()
        self.generate_new_lab()

    def create_widgets(self):
        self.main_frame = ttk.Frame(self.master, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.lab_title = ttk.Label(self.main_frame, text="", anchor="center")
        self.lab_title.pack(pady=10, fill=tk.X)

        self.lab_text = scrolledtext.ScrolledText(
            self.main_frame, 
            wrap=tk.WORD, 
            width=110, 
            height=38, 
            font=("Courier", 10), 
            bg="#34495e", 
            fg="#ecf0f1"
        )
        self.lab_text.pack(pady=10, fill=tk.BOTH, expand=True)

        self.finish_button = ttk.Button(self.main_frame, text="Finish", command=self.generate_new_lab)
        self.finish_button.pack(pady=10)

    def generate_new_lab(self):
        self.current_service = random.choice(self.services)
        self.unique_id = str(uuid.uuid4())[:8]
        lab_content = self.create_lab_content()
        self.lab_title.config(text=f"AWS CLI Lab: {self.current_service}")
        self.lab_text.delete(1.0, tk.END)
        self.lab_text.insert(tk.END, lab_content)
        self.insert_copy_buttons()

    def create_lab_content(self):
        content = f"In this lab, you'll learn how to use the AWS CLI to interact with {self.current_service}. Follow the steps below:\n\n"
        steps = self.get_service_steps()
        for i, step in enumerate(steps, 1):
            content += f"{i}. {step['description']}\n"
            content += f"   Command: {step['command']}\n\n"
        return content

    def get_service_steps(self):
        if self.current_service == "EC2":
            return [
                {"description": "Create a VPC", "command": f"aws ec2 create-vpc --cidr-block 10.0.0.0/16 --tag-specification 'ResourceType=vpc,Tags=[{{Key=Name,Value=MyVPC-{self.unique_id}}}]'"},
                {"description": "Create a subnet", "command": f"aws ec2 create-subnet --vpc-id vpc-XXXXXXXXXXXXXXXXX --cidr-block 10.0.1.0/24 --availability-zone us-west-2a"},
                {"description": "Create an Internet Gateway", "command": f"aws ec2 create-internet-gateway --tag-specification 'ResourceType=internet-gateway,Tags=[{{Key=Name,Value=MyIGW-{self.unique_id}}}]'"},
                {"description": "Attach Internet Gateway to VPC", "command": "aws ec2 attach-internet-gateway --vpc-id vpc-XXXXXXXXXXXXXXXXX --internet-gateway-id igw-XXXXXXXXXXXXXXXXX"},
                {"description": "Create a Route Table", "command": f"aws ec2 create-route-table --vpc-id vpc-XXXXXXXXXXXXXXXXX --tag-specification 'ResourceType=route-table,Tags=[{{Key=Name,Value=MyRouteTable-{self.unique_id}}}]'"},
                {"description": "Create a route to the Internet Gateway", "command": "aws ec2 create-route --route-table-id rtb-XXXXXXXXXXXXXXXXX --destination-cidr-block 0.0.0.0/0 --gateway-id igw-XXXXXXXXXXXXXXXXX"},
                {"description": "Associate the Route Table with the Subnet", "command": "aws ec2 associate-route-table --subnet-id subnet-XXXXXXXXXXXXXXXXX --route-table-id rtb-XXXXXXXXXXXXXXXXX"},
                {"description": "Create a Security Group", "command": f"aws ec2 create-security-group --group-name MySecurityGroup-{self.unique_id} --description 'My security group' --vpc-id vpc-XXXXXXXXXXXXXXXXX"},
                {"description": "Add inbound rule to Security Group", "command": "aws ec2 authorize-security-group-ingress --group-id sg-XXXXXXXXXXXXXXXXX --protocol tcp --port 22 --cidr 0.0.0.0/0"},
                {"description": "Launch an EC2 instance", "command": "aws ec2 run-instances --image-id ami-XXXXXXXXXXXXXXXXX --count 1 --instance-type t2.micro --key-name MyKeyPair --security-group-ids sg-XXXXXXXXXXXXXXXXX --subnet-id subnet-XXXXXXXXXXXXXXXXX"}
            ]
        elif self.current_service == "S3":
            bucket_name = f"my-unique-bucket-{self.unique_id}"
            return [
                {"description": "Create an S3 bucket", "command": f"aws s3api create-bucket --bucket {bucket_name} --region us-west-2 --create-bucket-configuration LocationConstraint=us-west-2"},
                {"description": "Enable versioning on the bucket", "command": f"aws s3api put-bucket-versioning --bucket {bucket_name} --versioning-configuration Status=Enabled"},
                {"description": "Upload a file to the bucket", "command": f"aws s3 cp example.html s3://{bucket_name}/"},
                {"description": "List objects in the bucket", "command": f"aws s3 ls s3://{bucket_name}"},
                {"description": "Download a file from the bucket", "command": f"aws s3 cp s3://{bucket_name}/example.html ./downloaded_example.html"},
                {"description": "Create a bucket policy", "command": f"aws s3api put-bucket-policy --bucket {bucket_name} --policy file://bucket_policy.json"},
                {"description": "Enable bucket encryption", "command": f"aws s3api put-bucket-encryption --bucket {bucket_name} --server-side-encryption-configuration '{{\"Rules\": [{{\"ApplyServerSideEncryptionByDefault\": {{\"SSEAlgorithm\": \"AES256\"}}}}]}}'"},
                {"description": "Create a lifecycle rule", "command": f"aws s3api put-bucket-lifecycle-configuration --bucket {bucket_name} --lifecycle-configuration file://lifecycle_config.json"},
                {"description": "Enable bucket logging", "command": f"aws s3api put-bucket-logging --bucket {bucket_name} --bucket-logging-status '{{\"LoggingEnabled\": {{\"TargetBucket\": \"{bucket_name}\", \"TargetPrefix\": \"logs/\"}}}}'"},
                {"description": "Delete objects from the bucket", "command": f"aws s3 rm s3://{bucket_name} --recursive"}
            ]
        elif self.current_service == "RDS":
            db_instance_id = f"mydb-{self.unique_id}"
            return [
                {"description": "Create a DB subnet group", "command": f"aws rds create-db-subnet-group --db-subnet-group-name mydbsubnetgroup --db-subnet-group-description 'My DB Subnet Group' --subnet-ids subnet-XXXXXXXXXXXXXXXXX subnet-YYYYYYYYYYYYYYYYY"},
                {"description": "Create an RDS instance", "command": f"aws rds create-db-instance --db-instance-identifier {db_instance_id} --db-instance-class db.t3.micro --engine mysql --master-username admin --master-user-password secret99 --allocated-storage 20 --db-subnet-group-name mydbsubnetgroup"},
                {"description": "Describe the RDS instance", "command": f"aws rds describe-db-instances --db-instance-identifier {db_instance_id}"},
                {"description": "Create a DB snapshot", "command": f"aws rds create-db-snapshot --db-snapshot-identifier mydbsnapshot-{self.unique_id} --db-instance-identifier {db_instance_id}"},
                {"description": "Modify the RDS instance", "command": f"aws rds modify-db-instance --db-instance-identifier {db_instance_id} --backup-retention-period 7 --apply-immediately"},
                {"description": "Create a read replica", "command": f"aws rds create-db-instance-read-replica --db-instance-identifier {db_instance_id}-replica --source-db-instance-identifier {db_instance_id}"},
                {"description": "List DB parameter groups", "command": "aws rds describe-db-parameter-groups"},
                {"description": "Create a DB parameter group", "command": f"aws rds create-db-parameter-group --db-parameter-group-name mydbparametergroup-{self.unique_id} --db-parameter-group-family mysql8.0 --description 'My DB Parameter Group'"},
                {"description": "Modify DB parameters", "command": f"aws rds modify-db-parameter-group --db-parameter-group-name mydbparametergroup-{self.unique_id} --parameters 'ParameterName=max_connections,ParameterValue=250,ApplyMethod=immediate'"},
                {"description": "Delete the RDS instance", "command": f"aws rds delete-db-instance --db-instance-identifier {db_instance_id} --skip-final-snapshot --delete-automated-backups"}
            ]
        elif self.current_service == "Lambda":
            function_name = f"my-function-{self.unique_id}"
            return [
                {"description": "Create a Lambda function", "command": f"aws lambda create-function --function-name {function_name} --runtime python3.8 --role arn:aws:iam::ACCOUNT_ID:role/lambda-ex --handler index.handler --zip-file fileb://function.zip"},
                {"description": "Invoke the Lambda function", "command": f"aws lambda invoke --function-name {function_name} --payload '{{\"key1\":\"value1\"}}' response.json"},
                {"description": "List Lambda functions", "command": "aws lambda list-functions"},
                {"description": "Update Lambda function code", "command": f"aws lambda update-function-code --function-name {function_name} --zip-file fileb://updated_function.zip"},
                {"description": "Publish a version", "command": f"aws lambda publish-version --function-name {function_name}"},
                {"description": "Create an alias", "command": f"aws lambda create-alias --function-name {function_name} --name prod --function-version 1"},
                {"description": "Add permissions to Lambda function", "command": f"aws lambda add-permission --function-name {function_name} --statement-id s3-put --action lambda:InvokeFunction --principal s3.amazonaws.com --source-arn arn:aws:s3:::mybucket"},
                {"description": "Create an event source mapping", "command": f"aws lambda create-event-source-mapping --function-name {function_name} --event-source-arn arn:aws:sqs:REGION:ACCOUNT_ID:myQueue"},
                {"description": "Get Lambda function configuration", "command": f"aws lambda get-function-configuration --function-name {function_name}"},
                {"description": "Delete the Lambda function", "command": f"aws lambda delete-function --function-name {function_name}"}
            ]
        elif self.current_service == "ECS":
            cluster_name = f"my-cluster-{self.unique_id}"
            return [
                {"description": "Create an ECS cluster", "command": f"aws ecs create-cluster --cluster-name {cluster_name}"},
                {"description": "Register a task definition", "command": "aws ecs register-task-definition --cli-input-json file://task-definition.json"},
                {"description": "List ECS clusters", "command": "aws ecs list-clusters"},
                {"description": "Describe the ECS cluster", "command": f"aws ecs describe-clusters --clusters {cluster_name}"},
                {"description": "Create an ECS service", "command": f"aws ecs create-service --cluster {cluster_name} --service-name my-service --task-definition my-task:1 --desired-count 2"},
                {"description": "List services in the cluster", "command": f"aws ecs list-services --cluster {cluster_name}"},
                {"description": "Describe ECS services", "command": f"aws ecs describe-services --cluster {cluster_name} --services my-service"},
                {"description": "Update ECS service", "command": f"aws ecs update-service --cluster {cluster_name} --service my-service --task-definition my-task:2"},
                {"description": "Run a task", "command": f"aws ecs run-task --cluster {cluster_name} --task-definition my-task:1 --count 1"},
                {"description": "Delete the ECS service", "command": f"aws ecs delete-service --cluster {cluster_name} --service my-service --force"}
            ]

    def copy_command(self, command):
        pyperclip.copy(command)
        self.show_copied_message()

    def show_copied_message(self):
        copied_label = ttk.Label(self.main_frame, text="Command copied!", foreground="#2ecc71", background="#34495e")
        copied_label.pack(pady=5)
        self.master.after(1500, copied_label.destroy)

    def insert_copy_buttons(self):
        self.lab_text.tag_configure("copy_button", foreground="#3498db", underline=True)
        content = self.lab_text.get("1.0", tk.END)
        lines = content.split("\n")
        self.lab_text.delete(1.0, tk.END)

        for line in lines:
            if line.startswith("   Command: "):
                command = line.replace("   Command: ", "")
                self.lab_text.insert(tk.END, line + "\n")
                self.lab_text.insert(tk.END, "   ")
                self.lab_text.insert(tk.END, "[Copy Command]", "copy_button")
                self.lab_text.tag_bind("copy_button", "<Button-1>", lambda e, cmd=command: self.copy_command(cmd))
                self.lab_text.insert(tk.END, "\n\n")
            else:
                self.lab_text.insert(tk.END, line + "\n")

def main():
    root = tk.Tk()
    app = AWSCLILab(root)
    root.mainloop()

if __name__ == "__main__":
    main()
