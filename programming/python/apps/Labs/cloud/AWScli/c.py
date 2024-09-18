import tkinter as tk
from tkinter import ttk, scrolledtext
import random
import pyperclip

class AWSCLILab:
    def __init__(self, master):
        self.master = master
        self.master.title("Advanced AWS CLI Lab")
        self.master.geometry("1200x800")
        self.master.configure(bg="black")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="black")
        self.style.configure("TLabel", background="black", foreground="white", font=("Arial", 16, "bold"))
        self.style.configure("TButton", background="#3498db", foreground="white", font=("Arial", 10, "bold"), padding=5)
        self.style.map("TButton", background=[("active", "#2980b9")])

        self.labs = [self.create_lab1(), self.create_lab2(), self.create_lab3()]
        self.current_lab_index = 0

        self.create_widgets()
        self.show_current_lab()

    def create_widgets(self):
        self.main_frame = ttk.Frame(self.master, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.lab_title = ttk.Label(self.main_frame, text="", anchor="center")
        self.lab_title.pack(pady=10, fill=tk.X)

        self.lab_text = scrolledtext.ScrolledText(
            self.main_frame, 
            wrap=tk.WORD, 
            width=130, 
            height=38, 
            font=("Courier", 10, "bold"), 
            bg="black", 
            fg="white"
        )
        self.lab_text.pack(pady=10, fill=tk.BOTH, expand=True)
        self.lab_text.bind("<Double-Button-1>", self.copy_text)

        self.finish_button = ttk.Button(self.main_frame, text="Next Lab", command=self.next_lab)
        self.finish_button.pack(pady=10)

    def create_lab1(self):
        return {
            "title": "Advanced AWS CLI Lab 1: EKS and Kubernetes",
            "tasks": [
                {"description": "Create an EKS cluster", 
                 "command": "aws eks create-cluster --name my-eks-cluster --role-arn arn:aws:iam::111122223333:role/eks-cluster-role --resources-vpc-config subnetIds=subnet-12345678,subnet-87654321,securityGroupIds=sg-12345678"},
                {"description": "Update kubeconfig for the new cluster", 
                 "command": "aws eks get-token --cluster-name my-eks-cluster | kubectl apply -f -"},
                {"description": "Deploy a sample application to the cluster", 
                 "command": "kubectl apply -f https://raw.githubusercontent.com/kubernetes/examples/master/guestbook/all-in-one/guestbook-all-in-one.yaml"},
                {"description": "List all pods in the cluster", 
                 "command": "kubectl get pods --all-namespaces"},
                {"description": "Create an IAM OIDC provider for the cluster", 
                 "command": "eksctl utils associate-iam-oidc-provider --cluster my-eks-cluster --approve"}
            ]
        }

    def create_lab2(self):
        return {
            "title": "Advanced AWS CLI Lab 2: CloudFormation and SAM",
            "tasks": [
                {"description": "Create a CloudFormation stack", 
                 "command": "aws cloudformation create-stack --stack-name my-cf-stack --template-body file://my-template.yaml --parameters ParameterKey=KeyPairName,ParameterValue=my-key-pair ParameterKey=InstanceType,ParameterValue=t2.micro"},
                {"description": "Package a SAM application", 
                 "command": "sam package --template-file template.yaml --s3-bucket my-sam-bucket --output-template-file packaged.yaml"},
                {"description": "Deploy a SAM application", 
                 "command": "sam deploy --template-file packaged.yaml --stack-name my-sam-stack --capabilities CAPABILITY_IAM"},
                {"description": "List all exports in the CloudFormation stack", 
                 "command": "aws cloudformation list-exports"},
                {"description": "Create a change set for the CloudFormation stack", 
                 "command": "aws cloudformation create-change-set --stack-name my-cf-stack --change-set-name my-change-set --template-body file://updated-template.yaml --parameters ParameterKey=InstanceType,ParameterValue=t2.small"}
            ]
        }

    def create_lab3(self):
        return {
            "title": "Advanced AWS CLI Lab 3: DynamoDB and Lambda",
            "tasks": [
                {"description": "Create a DynamoDB table with on-demand capacity", 
                 "command": "aws dynamodb create-table --table-name Users --attribute-definitions AttributeName=UserId,AttributeType=S --key-schema AttributeName=UserId,KeyType=HASH --billing-mode PAY_PER_REQUEST"},
                {"description": "Create a Lambda function with environment variables", 
                 "command": "aws lambda create-function --function-name my-lambda-function --runtime python3.8 --role arn:aws:iam::111122223333:role/lambda-ex --handler app.lambda_handler --zip-file fileb://function.zip --environment Variables={DB_TABLE=Users,LOG_LEVEL=INFO}"},
                {"description": "Create an API Gateway REST API", 
                 "command": "aws apigateway create-rest-api --name 'My API' --description 'This is my API'"},
                {"description": "Add a DynamoDB stream to the table", 
                 "command": "aws dynamodb update-table --table-name Users --stream-specification StreamEnabled=true,StreamViewType=NEW_AND_OLD_IMAGES"},
                {"description": "Create an event source mapping for Lambda to process DynamoDB streams", 
                 "command": "aws lambda create-event-source-mapping --function-name my-lambda-function --event-source arn:aws:dynamodb:us-west-2:111122223333:table/Users/stream/2021-03-05T00:00:00.000 --batch-size 100 --starting-position LATEST"}
            ]
        }

    def show_current_lab(self):
        lab = self.labs[self.current_lab_index]
        self.lab_title.config(text=lab["title"])
        self.lab_text.delete(1.0, tk.END)
        for i, task in enumerate(lab["tasks"], 1):
            self.lab_text.insert(tk.END, f"{i}. {task['description']}\n")
            self.lab_text.insert(tk.END, f"   Command: {task['command']}\n\n")

    def next_lab(self):
        self.current_lab_index = (self.current_lab_index + 1) % len(self.labs)
        self.show_current_lab()

    def copy_text(self, event):
        try:
            text = self.lab_text.get("current linestart", "current lineend")
            if text.startswith("   Command: "):
                pyperclip.copy(text.replace("   Command: ", ""))
            else:
                pyperclip.copy(text.split(". ", 1)[1] if ". " in text else text)
        except Exception as e:
            print(f"Error copying text: {e}")

def main():
    root = tk.Tk()
    app = AWSCLILab(root)
    root.mainloop()

if __name__ == "__main__":
    main()
