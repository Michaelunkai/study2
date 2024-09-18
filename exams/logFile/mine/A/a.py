import os
import requests
import re
from tkinter import *
from tkinter import scrolledtext, messagebox
from datetime import datetime

# Function to download the log file with at least 5000 lines
def download_log_file():
    url = 'https://raw.githubusercontent.com/elastic/examples/master/Common%20Data%20Formats/nginx_logs/nginx_logs'
    response = requests.get(url)
    with open("exam.log", "w") as file:
        file.write(response.text)
    return "exam.log"

# Function to create the tasks for the exam
def create_exam_tasks():
    tasks = [
        "1. Count the number of lines that contain the word 'GET'.",
        "2. Find the most common status code in the log file.",
        "3. Calculate the total number of bytes transferred in all requests.",
        "4. Identify the IP address with the most requests.",
        "5. Count the number of requests made in the last hour of the log."
    ]
    return tasks

# Function to display tasks and allow pasting solutions
def start_exam():
    tasks = create_exam_tasks()
    for i, task in enumerate(tasks):
        task_label = Label(window, text=f"Task {i+1}: {task}")
        task_label.pack()
        task_textbox = scrolledtext.ScrolledText(window, width=100, height=10)
        task_textbox.pack()
        task_textboxes.append(task_textbox)

    submit_button.config(state=NORMAL)

# Function to evaluate the user's task submissions
def evaluate_exam():
    score = 0
    total_tasks = len(task_textboxes)
    log_file_path = "exam.log"
    
    # Task 1 evaluation: Count the number of lines containing 'GET'
    with open(log_file_path, 'r') as file:
        get_count = sum(1 for line in file if "GET" in line)
    user_solution_task_1 = task_textboxes[0].get("1.0", END).strip()
    if str(get_count) in user_solution_task_1:
        score += 20
    
    # Task 2 evaluation: Find the most common status code
    with open(log_file_path, 'r') as file:
        status_codes = re.findall(r'(\d{3})', file.read())
    if status_codes:
        most_common_status_code = max(set(status_codes), key=status_codes.count)
    else:
        most_common_status_code = None
    user_solution_task_2 = task_textboxes[1].get("1.0", END).strip()
    if most_common_status_code in user_solution_task_2:
        score += 20

    # Task 3 evaluation: Calculate the total number of bytes transferred
    with open(log_file_path, 'r') as file:
        bytes_transferred = sum(int(match.group(1)) for match in re.finditer(r'(\d+)$', file.read(), re.MULTILINE))
    user_solution_task_3 = task_textboxes[2].get("1.0", END).strip()
    if str(bytes_transferred) in user_solution_task_3:
        score += 20

    # Task 4 evaluation: Identify the IP address with the most requests
    with open(log_file_path, 'r') as file:
        ips = re.findall(r'(\d+\.\d+\.\d+\.\d+)', file.read())
    if ips:
        most_common_ip = max(set(ips), key=ips.count)
    else:
        most_common_ip = None
    user_solution_task_4 = task_textboxes[3].get("1.0", END).strip()
    if most_common_ip in user_solution_task_4:
        score += 20

    # Task 5 evaluation: Count the number of requests made in the last hour of the log
    with open(log_file_path, 'r') as file:
        lines = file.readlines()
    last_timestamp = lines[-1].split('[')[1].split(']')[0] if lines else None
    if last_timestamp:
        last_hour = datetime.strptime(last_timestamp, "%d/%b/%Y:%H:%M:%S %z").hour
        requests_last_hour = sum(1 for line in lines if datetime.strptime(line.split('[')[1].split(']')[0], "%d/%b/%Y:%H:%M:%S %z").hour == last_hour)
    else:
        requests_last_hour = 0
    user_solution_task_5 = task_textboxes[4].get("1.0", END).strip()
    if str(requests_last_hour) in user_solution_task_5:
        score += 20

    messagebox.showinfo("Exam Result", f"Your score is: {score}/100")

# Function to start the application
def start_application():
    log_file_label.config(text="Downloading log file...")
    log_file = download_log_file()
    if os.path.exists(log_file):
        log_file_label.config(text=f"Log file downloaded successfully: {log_file}")
    start_exam()

# GUI setup using Tkinter
window = Tk()
window.title("Log File Exam Application")
window.geometry('800x600')

task_textboxes = []

log_file_label = Label(window, text="Click 'Start Exam' to begin")
log_file_label.pack()

start_button = Button(window, text="Start Exam", command=start_application)
start_button.pack()

submit_button = Button(window, text="Submit Exam", command=evaluate_exam, state=DISABLED)
submit_button.pack()

window.mainloop()
