import tkinter as tk
from tkinter import messagebox, scrolledtext
import random
import boto3
import subprocess
import sys
import uuid

class AWSCLILab:
    def __init__(self, master):
        self.master = master
        self.master.title("AWS CLI Lab")
        self.master.geometry("1000x700")

        self.services = [
            "S3", "EC2", "Lambda", "DynamoDB", "CloudFormation",
            "IAM", "RDS", "SNS", "SQS", "CloudWatch"
        ]
        self.current_service = None
        self.unique_id = str(uuid.uuid4())[:8]

        self.create_widgets()
        self.generate_new_lab()

    def create_widgets(self):
        self.lab_text = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, width=120, height=40)
        self.lab_text.pack(pady=10)

        self.finish_button = tk.Button(self.master, text="Finish", command=self.generate_new_lab)
        self.fini _button.pack(pady=10)

    def generate_new_lab(self):
        self.current_service = random.choice(self.services)
        lab_content = self.create_lab_content()
        self.lab_text.delete(1.0, tk.END)
        self.lab_text.insert(tk.END, lab_content)

    def create_lab_content(self):
        content = f"AWS CLI Lab: {self.current_service}\n\n"
        content += "In this lab, you'll learn how to use the AWS CLI to interact with " \
                   f"{self.current_service}. Follow the steps below:\n\n"

        steps = self.get_service_steps()
        for i, step in enumerate(steps, 1):
            content += f"{i}. {step}\n\n"

        content += "\nAfter completing the lab, click the 'Finish' button to generate a new lab."
        return content

    def get_service_steps(self):
        if self.current_service == "S3":
            bucket_name = f"my-unique-bucket-{self.unique_id}"
            return [
                f"Create a new S3 bucket:\naws s3 mb s3://{bucket_name}",
                f"Upload a file to the bucket:\naws s3 cp example.txt s3://{bucket_name}/",
                f"List the contents of the bucket:\naws s3 ls s3://{bucket_name}",
                f"Download a file from the bucket:\naws s3 cp s3://{bucket_name}/example.txt downloaded_example.txt",
                f"Delete a file from the bucket:\naws s3 rm s3://{bucket_name}/example.txt",
                f"Remove the bucket:\naws s3 rb s3://{bucket_name} --force"
            ]
        elif self.current_service == "EC2":
            return [
                "Create a key pair:\naws ec2 create-key-pair --key-name MyKeyPair --query 'KeyMaterial' --output text > MyKeyPair.pem",
                "Create a security group:\naws ec2 create-security-group --group-name MySecurityGroup --description 'My security group'",
                "Add an inbound rule to the security group:\naws ec2 authorize-security-group-ingress --group-name MySecurityGroup --protocol tcp --port 22 --cidr 0.0.0.0/0",
                "Launch an EC2 instance (replace ami-xxxxxxxx with a valid AMI ID for your region):\naws ec2 run-instances --image-id ami-xxxxxxxx --count 1 --instance-type t2.micro --key-name MyKeyPair --security-group-ids sg-xxxxxxxxxxxxxxxxx",
                "Describe the instance (replace i-xxxxxxxxxxxxxxxxx with your instance ID):\naws ec2 describe-instances --instance-ids i-xxxxxxxxxxxxxxxxx",
                "Stop the instance:\naws ec2 stop-instances --instance-ids i-xxxxxxxxxxxxxxxxx",
                "Terminate the instance:\naws ec2 terminate-instances --instance-ids i-xxxxxxxxxxxxxxxxx"
            ]
        elif self.current_service == "Lambda":
            function_name = f"my-function-{self.unique_id}"
            return [
                "Create a Lambda function deployment package (zip file containing your code):\nzip function.zip index.py",
                "Create an IAM role for Lambda:\naws iam create-role --role-name lambda-ex --assume-role-policy-document '{\"Version\": \"2012-10-17\",\"Statement\": [{ \"Effect\": \"Allow\", \"Principal\": {\"Service\": \"lambda.amazonaws.com\"}, \"Action\": \"sts:AssumeRole\"}]}'",
                "Attach permissions to the IAM role:\naws iam attach-role-policy --role-name lambda-ex --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
                f"Create a Lambda function (replace ACCOUNT_ID with your AWS account ID):\naws lambda create-function --function-name {function_name} --zip-file fileb://function.zip --handler index.handler --runtime python3.8 --role arn:aws:iam::ACCOUNT_ID:role/lambda-ex",
                f"Invoke the Lambda function:\naws lambda invoke --function-name {function_name} --payload '{{}}' output.txt",
                f"Update the Lambda function code:\naws lambda update-function-code --function-name {function_name} --zip-file fileb://function-updated.zip",
                f"Delete the Lambda function:\naws lambda delete-function --function-name {function_name}"
            ]
        elif self.current_service == "DynamoDB":
            table_name = f"MyTable-{self.unique_id}"
            return [
                f"Create a DynamoDB table:\naws dynamodb create-table --table-name {table_name} --attribute-definitions AttributeName=ID,AttributeType=S --key-schema AttributeName=ID,KeyType=HASH --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5",
                "List DynamoDB tables:\naws dynamodb list-tables",
                f"Put an item in the table:\naws dynamodb put-item --table-name {table_name} --item '{{\"ID\": {{\"S\": \"001\"}}, \"Name\": {{\"S\": \"John Doe\"}}}}'",
                f"Get an item from the table:\naws dynamodb get-item --table-name {table_name} --key '{{\"ID\": {{\"S\": \"001\"}}}}'",
                f"Scan the table:\naws dynamodb scan --table-name {table_name}",
                f"Delete an item from the table:\naws dynamodb delete-item --table-name {table_name} --key '{{\"ID\": {{\"S\": \"001\"}}}}'",
                f"Delete the DynamoDB table:\naws dynamodb delete-table --table-name {table_name}"
            ]
        elif self.current_service == "CloudFormation":
            stack_name = f"MyStack-{self.unique_id}"
            return [
                "Create a CloudFormation template file (e.g., template.yaml)",
                "Validate the CloudFormation template:\naws cloudformation validate-template --template-body file://template.yaml",
                f"Create a CloudFormation stack:\naws cloudformation create-stack --stack-name {stack_name} --template-body file://template.yaml",
                f"Describe the CloudFormation stack:\naws cloudformation describe-stacks --stack-name {stack_name}",
                f"List stack resources:\naws cloudformation list-stack-resources --stack-name {stack_name}",
                f"Update the CloudFormation stack:\naws cloudformation update-stack --stack-name {stack_name} --template-body file://updated-template.yaml",
                f"Delete the CloudFormation stack:\naws cloudformation delete-stack --stack-name {stack_name}"
            ]
        elif self.current_service == "IAM":
            user_name = f"TestUser-{self.unique_id}"
            group_name = f"TestGroup-{self.unique_id}"
            policy_name = f"TestPolicy-{self.unique_id}"
            return [
                f"Create an IAM user:\naws iam create-user --user-name {user_name}",
                f"Create an IAM group:\naws iam create-group --group-name {group_name}",
                f"Add user to the group:\naws iam add-user-to-group --user-name {user_name} --group-name {group_name}",
                f"Create an IAM policy:\naws iam create-policy --policy-name {policy_name} --policy-document file://policy.json",
                f"Attach policy to the group:\naws iam attach-group-policy --group-name {group_name} --policy-arn arn:aws:iam::ACCOUNT_ID:policy/{policy_name}",
                f"List users:\naws iam list-users",
                f"List groups:\naws iam list-groups",
                f"Remove user from group:\naws iam remove-user-from-group --user-name {user_name} --group-name {group_name}",
                f"Delete user:\naws iam delete-user --user-name {user_name}",
                f"Delete group:\naws iam delete-group --group-name {group_name}",
                f"Delete policy:\naws iam delete-policy --policy-arn arn:aws:iam::ACCOUNT_ID:policy/{policy_name}"
            ]
        elif self.current_service == "RDS":
            db_instance_id = f"mydb-{self.unique_id}"
            return [
                f"Create an RDS instance:\naws rds create-db-instance --db-instance-identifier {db_instance_id} --db-instance-class db.t3.micro --engine mysql --master-username admin --master-user-password secret99 --allocated-storage 20",
                f"Describe the RDS instance:\naws rds describe-db-instances --db-instance-identifier {db_instance_id}",
                f"Modify the RDS instance:\naws rds modify-db-instance --db-instance-identifier {db_instance_id} --backup-retention-period 7",
                f"Create a snapshot:\naws rds create-db-snapshot --db-instance-identifier {db_instance_id} --db-snapshot-identifier my-snapshot",
                f"List snapshots:\naws rds describe-db-snapshots --db-instance-identifier {db_instance_id}",
                f"Delete the RDS instance:\naws rds delete-db-instance --db-instance-identifier {db_instance_id} --skip-final-snapshot"
            ]
        elif self.current_service == "SNS":
            topic_name = f"MyTopic-{self.unique_id}"
            return [
                f"Create an SNS topic:\naws sns create-topic --name {topic_name}",
                f"List SNS topics:\naws sns list-topics",
                f"Subscribe an email to the topic (replace YOUR_EMAIL with a valid email address):\naws sns subscribe --topic-arn arn:aws:sns:REGION:ACCOUNT_ID:{topic_name} --protocol email --notification-endpoint YOUR_EMAIL",
                f"Publish a message to the topic:\naws sns publish --topic-arn arn:aws:sns:REGION:ACCOUNT_ID:{topic_name} --message 'Hello from AWS CLI'",
                f"List subscriptions:\naws sns list-subscriptions-by-topic --topic-arn arn:aws:sns:REGION:ACCOUNT_ID:{topic_name}",
                f"Delete the SNS topic:\naws sns delete-topic --topic-arn arn:aws:sns:REGION:ACCOUNT_ID:{topic_name}"
            ]
        elif self.current_service == "SQS":
            queue_name = f"MyQueue-{self.unique_id}"
            return [
                f"Create an SQS queue:\naws sqs create-queue --queue-name {queue_name}",
                "List SQS queues:\naws sqs list-queues",
                f"Send a message to the queue:\naws sqs send-message --queue-url https://sqs.REGION.amazonaws.com/ACCOUNT_ID/{queue_name} --message-body 'Hello from AWS CLI'",
                f"Receive messages from the queue:\naws sqs receive-message --queue-url https://sqs.REGION.amazonaws.com/ACCOUNT_ID/{queue_name}",
                f"Delete a message from the queue (replace RECEIPT_HANDLE with the actual receipt handle):\naws sqs delete-message --queue-url https://sqs.REGION.amazonaws.com/ACCOUNT_ID/{queue_name} --receipt-handle RECEIPT_HANDLE",
                f"Delete the SQS queue:\naws sqs delete-queue --queue-url https://sqs.REGION.amazonaws.com/ACCOUNT_ID/{queue_name}"
            ]
        elif self.current_service == "CloudWatch":
            alarm_name = f"MyAlarm-{self.unique_id}"
            return [
                f"Create a CloudWatch alarm:\naws cloudwatch put-metric-alarm --alarm-name {alarm_name} --alarm-description 'Test alarm' --metric-name CPUUtilization --namespace AWS/EC2 --statistic Average --period 300 --threshold 70 --comparison-operator GreaterThanThreshold --dimensions Name=InstanceId,Value=i-12345678 --evaluation-periods 2 --alarm-actions arn:aws:sns:REGION:ACCOUNT_ID:MyTopic",
                "List CloudWatch alarms:\naws cloudwatch describe-alarms",
                f"Describe a specific alarm:\naws cloudwatch describe-alarms --alarm-names {alarm_name}",
                "Get metric statistics:\naws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name CPUUtilization --dimensions Name=InstanceId,Value=i-12345678 --start-time 2023-01-01T00:00:00Z --end-time 2023-01-02T00:00:00Z --period 3600 --statistics Average",
                f"Delete the CloudWatch alarm:\naws cloudwatch delete-alarms --alarm-names {alarm_name}"
            ]
        else:
            return [
                f"List {self.current_service} resources:\naws {self.current_service.lower()} help",
                f"Create a {self.current_service} resource:\naws {self.current_service.lower()} create-resource --name my-resource",
                f"Describe {self.current_service} resources:\naws {self.current_service.lower()} describe-resources",
                f"Update a {self.current_service} resource:\naws {self.current_service.lower()} update-resource --resource-id resource-id --new-config new-config",
                f"Delete a {self.current_service} resource:\naws {self.current_service.lower()} delete-resource --resource-id resource-id"
            ]

def main():
    root = tk.Tk()
    app = AWSCLILab(root)
    root.mainloop()

if __name__ == "__main__":
    main()
