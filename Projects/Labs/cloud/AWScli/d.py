import tkinter as tk
from tkinter import ttk, scrolledtext
import pyperclip

class AWSCLILab:
    def __init__(self, master):
        self.master = master
        self.master.title("Advanced AWS CLI Lab")
        self.master.geometry("1400x900")
        self.master.configure(bg="black")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="black")
        self.style.configure("TLabel", background="black", foreground="white", font=("Arial", 16, "bold"))
        self.style.configure("BigButton.TButton", background="#3498db", foreground="white", font=("Arial", 14, "bold"), padding=10)
        self.style.map("BigButton.TButton", background=[("active", "#2980b9")])

        self.labs = [self.create_rds_lab(), self.create_cloudfront_lab(), self.create_sns_lab()]
        self.current_lab_index = 0

        self.create_widgets()
        self.show_current_lab()

    def create_widgets(self):
        self.main_frame = ttk.Frame(self.master, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.title_frame = ttk.Frame(self.main_frame)
        self.title_frame.pack(fill=tk.X, pady=10)

        self.lab_title = ttk.Label(self.title_frame, text="", anchor="center")
        self.lab_title.pack(side=tk.LEFT, expand=True)

        self.next_button = ttk.Button(self.title_frame, text="Next Lab", command=self.next_lab, style="BigButton.TButton")
        self.next_button.pack(side=tk.RIGHT, padx=10)

        self.lab_text = scrolledtext.ScrolledText(
            self.main_frame, 
            wrap=tk.WORD, 
            width=150, 
            height=45,
            font=("Courier", 10, "bold"), 
            bg="black", 
            fg="white"
        )
        self.lab_text.pack(pady=10, fill=tk.BOTH, expand=True)
        self.lab_text.bind("<Double-Button-1>", self.copy_text)

    def create_rds_lab(self):
        return {
            "title": "Advanced AWS CLI Lab: RDS Operations",
            "tasks": [
                {"description": "Create a DB subnet group", 
                 "command": "aws rds create-db-subnet-group --db-subnet-group-name mydbsubnetgroup --db-subnet-group-description \"My DB Subnet Group\" --subnet-ids subnet-12345678 subnet-87654321"},
                {"description": "Create an RDS instance", 
                 "command": "aws rds create-db-instance --db-instance-identifier mydbinstance --db-instance-class db.t3.micro --engine mysql --master-username admin --master-user-password mypassword123 --allocated-storage 20 --db-subnet-group-name mydbsubnetgroup"},
                {"description": "Create a DB snapshot", 
                 "command": "aws rds create-db-snapshot --db-instance-identifier mydbinstance --db-snapshot-identifier mydbsnapshot"},
                {"description": "Modify the RDS instance", 
                 "command": "aws rds modify-db-instance --db-instance-identifier mydbinstance --backup-retention-period 7 --apply-immediately"},
                {"description": "Create a read replica", 
                 "command": "aws rds create-db-instance-read-replica --db-instance-identifier mydbinstance-replica --source-db-instance-identifier mydbinstance"},
                {"description": "Describe DB instances", 
                 "command": "aws rds describe-db-instances"},
                {"description": "Create a DB parameter group", 
                 "command": "aws rds create-db-parameter-group --db-parameter-group-name mydbparametergroup --db-parameter-group-family mysql8.0 --description \"My DB Parameter Group\""},
                {"description": "Delete the RDS instance", 
                 "command": "aws rds delete-db-instance --db-instance-identifier mydbinstance --skip-final-snapshot"}
            ]
        }

    def create_cloudfront_lab(self):
        return {
            "title": "Advanced AWS CLI Lab: CloudFront Operations",
            "tasks": [
                {"description": "Create a CloudFront distribution", 
                 "command": "aws cloudfront create-distribution --distribution-config file://distribution-config.json"},
                {"description": "List CloudFront distributions", 
                 "command": "aws cloudfront list-distributions"},
                {"description": "Get distribution config", 
                 "command": "aws cloudfront get-distribution-config --id EXXXXXXXXXXXXX"},
                {"description": "Update distribution", 
                 "command": "aws cloudfront update-distribution --id EXXXXXXXXXXXXX --distribution-config file://updated-config.json --if-match EXXXXXXXXXXXXX"},
                {"description": "Create a CloudFront origin access identity", 
                 "command": "aws cloudfront create-cloud-front-origin-access-identity --cloud-front-origin-access-identity-config '{\"CallerReference\": \"my-access-identity\", \"Comment\": \"My OAI\"}'"},
                {"description": "Create a CloudFront cache policy", 
                 "command": "aws cloudfront create-cache-policy --cache-policy-config file://cache-policy-config.json"},
                {"description": "Create a CloudFront function", 
                 "command": "aws cloudfront create-function --name my-function --function-config '{\"Comment\":\"My function\",\"Runtime\":\"cloudfront-js-1.0\"}' --function-code fileb://function.js"},
                {"description": "Delete the CloudFront distribution", 
                 "command": "aws cloudfront delete-distribution --id EXXXXXXXXXXXXX --if-match EXXXXXXXXXXXXX"}
            ]
        }

    def create_sns_lab(self):
        return {
            "title": "Advanced AWS CLI Lab: SNS Operations",
            "tasks": [
                {"description": "Create an SNS topic", 
                 "command": "aws sns create-topic --name my-topic"},
                {"description": "Subscribe an email to the topic", 
                 "command": "aws sns subscribe --topic-arn arn:aws:sns:us-west-2:123456789012:my-topic --protocol email --notification-endpoint user@example.com"},
                {"description": "Publish a message to the topic", 
                 "command": "aws sns publish --topic-arn arn:aws:sns:us-west-2:123456789012:my-topic --message \"Hello from SNS!\""},
                {"description": "List subscriptions", 
                 "command": "aws sns list-subscriptions"},
                {"description": "Set topic attributes", 
                 "command": "aws sns set-topic-attributes --topic-arn arn:aws:sns:us-west-2:123456789012:my-topic --attribute-name DisplayName --attribute-value \"My Display Name\""},
                {"description": "Create an SNS platform application", 
                 "command": "aws sns create-platform-application --name my-application --platform GCM --attributes '{\"PlatformCredential\": \"your_api_key\"}'"},
                {"description": "Create a platform endpoint", 
                 "command": "aws sns create-platform-endpoint --platform-application-arn arn:aws:sns:us-west-2:123456789012:app/GCM/my-application --token device_token"},
                {"description": "Delete the SNS topic", 
                 "command": "aws sns delete-topic --topic-arn arn:aws:sns:us-west-2:123456789012:my-topic"}
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
