import os
import requests
import re
from tkinter import *
from tkinter import scrolledtext, messagebox
from tkinter import ttk
from datetime import datetime
from collections import Counter
import threading
import ttkbootstrap as tb
from ttkbootstrap.constants import *

# Function to download the Apache log file with at least 5000 lines
def download_log_file():
    # Apache access log sample with over 5000 lines
    url = 'https://raw.githubusercontent.com/elastic/examples/master/Common%20Data%20Formats/apache_logs/apache_logs'
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status
    with open("apache_exam.log", "w", encoding='utf-8') as file:
        file.write(response.text)
    return "apache_exam.log"

# Function to create the tasks for the exam
def create_exam_tasks():
    tasks = [
        "1. Count the number of POST requests in the log file.",
        "2. Identify the top 10 IP addresses by the number of requests made.",
        "3. Determine the most requested resource (URL) in the log file.",
        "4. Calculate the percentage of successful requests (status code 200).",
        "5. List the top 5 referrers from the log file."
    ]
    return tasks

# Function to start the exam
def start_exam():
    threading.Thread(target=load_exam).start()

def load_exam():
    # Disable start button and show loading
    start_button.config(state=DISABLED)
    progress_label.config(text="Downloading log file and loading tasks, please wait...")
    
    # Download log file
    try:
        log_file = download_log_file()
        if os.path.exists(log_file):
            progress_label.config(text="Log file downloaded successfully.")
        else:
            progress_label.config(text="Failed to download log file.")
            return
    except Exception as e:
        progress_label.config(text=f"Error downloading log file: {e}")
        return
    
    # Clear any existing widgets in the main frame
    for widget in main_frame.winfo_children():
        widget.destroy()
    
    # Create a canvas and scrollbar for the tasks
    canvas = Canvas(main_frame, bg="#f8f9fa")
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="#f8f9fa")
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    # Display tasks and input areas
    tasks = create_exam_tasks()
    for i, task in enumerate(tasks):
        task_label = tb.Label(
            scrollable_frame, 
            text=task, 
            font=("Helvetica", 12, "bold"), 
            anchor="w", 
            wraplength=750, 
            bootstyle="info"
        )
        task_label.pack(fill=X, padx=20, pady=(10 if i == 0 else 5, 2))
        
        # Bind double-click to copy task text
        task_label.bind("<Double-Button-1>", lambda e, text=task: copy_to_clipboard(text))
        
        task_textbox = scrolledtext.ScrolledText(
            scrollable_frame, 
            width=100, 
            height=7, 
            font=("Consolas", 10), 
            wrap=WORD
        )
        task_textbox.pack(padx=20, pady=5)
        task_textboxes.append(task_textbox)
    
    # Enable submit button
    submit_button.config(state=NORMAL)
    progress_label.config(text="Tasks loaded. You may begin your exam.")

# Function to copy text to clipboard
def copy_to_clipboard(text):
    window.clipboard_clear()
    window.clipboard_append(text)
    messagebox.showinfo("Copied", "Task description copied to clipboard.")

# Function to evaluate the user's task submissions
def evaluate_exam():
    score = 0
    feedback = []
    log_file_path = "apache_exam.log"
    
    # Task 1 evaluation: Count the number of POST requests
    with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as file:
        post_count = sum(1 for line in file if 'POST' in line)
    user_solution_task_1 = task_textboxes[0].get("1.0", END).strip()
    try:
        user_post_count = int(user_solution_task_1)
        if user_post_count == post_count:
            score += 20
            feedback.append("**Task 1:** Correct. The number of POST requests matches.")
        elif abs(user_post_count - post_count) <= 5:  # Allow small margin
            score += 15
            feedback.append(f"**Task 1:** Partially correct. Expected approximately {post_count}, but got {user_post_count}.")
        else:
            feedback.append(f"**Task 1:** Incorrect. Expected {post_count}, but got {user_post_count}.")
    except ValueError:
        feedback.append("**Task 1:** Incorrect. Please enter a valid integer.")
    
    # Task 2 evaluation: Identify the top 10 IP addresses by number of requests
    with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as file:
        ips = re.findall(r'^(\d+\.\d+\.\d+\.\d+)', file.read(), re.MULTILINE)
    ip_counts = Counter(ips)
    top_10_ips = [ip for ip, count in ip_counts.most_common(10)]
    user_solution_task_2 = task_textboxes[1].get("1.0", END).strip().split('\n')
    user_top_10_ips = [ip.strip() for ip in user_solution_task_2 if ip.strip()]
    if user_top_10_ips == top_10_ips:
        score += 20
        feedback.append("**Task 2:** Correct. The top 10 IP addresses match.")
    elif set(user_top_10_ips).issubset(set(top_10_ips)):
        score += 15
        feedback.append("**Task 2:** Partially correct. Some IPs are correct.")
    else:
        feedback.append("**Task 2:** Incorrect. The top 10 IP addresses do not match.")
    
    # Task 3 evaluation: Determine the most requested resource (URL)
    with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as file:
        urls = re.findall(r'\"[A-Z]+\s+([^ ]+)\s+HTTP', file.read())
    if urls:
        most_requested_url, count = Counter(urls).most_common(1)[0]
    else:
        most_requested_url = None
    user_solution_task_3 = task_textboxes[2].get("1.0", END).strip()
    if user_solution_task_3 == most_requested_url:
        score += 20
        feedback.append("**Task 3:** Correct. The most requested resource matches.")
    else:
        score += 0
        feedback.append(f"**Task 3:** Incorrect. Expected '{most_requested_url}', but got '{user_solution_task_3}'.")
    
    # Task 4 evaluation: Calculate the percentage of successful requests (status code 200)
    with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as file:
        total_requests = 0
        success_requests = 0
        for line in file:
            total_requests += 1
            status_code_match = re.search(r'\" (\d{3}) ', line)
            if status_code_match and status_code_match.group(1) == '200':
                success_requests += 1
    percentage_success = (success_requests / total_requests) * 100 if total_requests > 0 else 0
    user_solution_task_4 = task_textboxes[3].get("1.0", END).strip().replace('%','')
    try:
        user_percentage_success = float(user_solution_task_4)
        if abs(user_percentage_success - percentage_success) < 0.1:
            score += 20
            feedback.append("**Task 4:** Correct. The percentage of successful requests matches.")
        elif abs(user_percentage_success - percentage_success) <= 2:
            score += 15
            feedback.append(f"**Task 4:** Partially correct. Expected approximately {percentage_success:.2f}%, but got {user_percentage_success}%.")
        else:
            feedback.append(f"**Task 4:** Incorrect. Expected {percentage_success:.2f}%, but got {user_percentage_success}%.")
    except ValueError:
        feedback.append("**Task 4:** Incorrect. Please enter a valid percentage.")
    
    # Task 5 evaluation: List the top 5 referrers
    with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as file:
        referrers = re.findall(r'\"[^"]+\" \"[^"]+\" \"([^"]+)\"', file.read())
    referrer_counts = Counter(referrers)
    top_5_referrers = [ref for ref, count in referrer_counts.most_common(5)]
    user_solution_task_5 = task_textboxes[4].get("1.0", END).strip().split('\n')
    user_top_5_referrers = [ref.strip() for ref in user_solution_task_5 if ref.strip()]
    if user_top_5_referrers == top_5_referrers:
        score += 20
        feedback.append("**Task 5:** Correct. The top 5 referrers match.")
    elif set(user_top_5_referrers).issubset(set(top_5_referrers)):
        score += 15
        feedback.append("**Task 5:** Partially correct. Some referrers are correct.")
    else:
        feedback.append("**Task 5:** Incorrect. The top 5 referrers do not match.")
    
    # Display the score and feedback
    detailed_feedback = "\n\n".join(feedback)
    final_message = f"Your total score is: {score}/100\n\nDetailed Feedback:\n{detailed_feedback}"
    messagebox.showinfo("Exam Result", final_message)
    
    # Reset the application for another attempt
    reset_application()

def reset_application():
    # Clear the main frame
    for widget in main_frame.winfo_children():
        widget.destroy()
    task_textboxes.clear()
    
    # Enable start button
    start_button.config(state=NORMAL)
    submit_button.config(state=DISABLED)
    progress_label.config(text="Click 'Start Exam' to begin.")

# Function to quit the application gracefully
def quit_application():
    if messagebox.askokcancel("Quit", "Do you want to quit the exam?"):
        window.destroy()

# GUI setup using ttkbootstrap
window = tb.Window(themename="superhero")  # You can choose other themes like 'cosmo', 'darkly', etc.
window.title("Apache Log File Analysis Exam")
window.geometry('1100x800')
window.resizable(True, True)
window.protocol("WM_DELETE_WINDOW", quit_application)

# Header frame
header_frame = Frame(window, bg="#2c3e50")  # Dark blue background
header_frame.pack(fill=X)

header_label = tb.Label(
    header_frame, 
    text="Apache Log File Analysis Exam", 
    font=("Helvetica", 24, "bold"), 
    anchor="center", 
    bootstyle="inverse"
)
header_label.pack(pady=20)

# Main frame with padding
main_frame = Frame(window, bg="#ecf0f1")  # Light grey background
main_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

# Progress label
progress_label = tb.Label(window, text="Click 'Start Exam' to begin.", font=("Helvetica", 14))
progress_label.pack(pady=10)

# Buttons frame
buttons_frame = Frame(window)
buttons_frame.pack(pady=10)

start_button = tb.Button(
    buttons_frame, 
    text="Start Exam", 
    command=start_exam, 
    bootstyle="success-outline", 
    width=15
)
start_button.grid(row=0, column=0, padx=10)

submit_button = tb.Button(
    buttons_frame, 
    text="Submit Exam", 
    command=evaluate_exam, 
    state=DISABLED, 
    bootstyle="danger-outline", 
    width=15
)
submit_button.grid(row=0, column=1, padx=10)

task_textboxes = []

# Run the application
window.mainloop()
