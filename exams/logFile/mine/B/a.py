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
        "1. Extract and list all unique user agents present in the log file.",
        "2. Calculate the percentage of requests that resulted in a 404 status code.",
        "3. Identify the top 5 URLs that have been requested the most.",
        "4. Find the busiest hour of the day in terms of number of requests.",
        "5. Determine the average size of requests in bytes."
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
    canvas = Canvas(main_frame, bg="#f0f0f0")
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="#f0f0f0")
    
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
    log_file_path = "exam.log"
    
    # Task 1 evaluation: Extract and list all unique user agents
    with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as file:
        user_agents = set(re.findall(r'\"[^\"]*\" \"([^\"]*)\"', file.read()))
    user_solution_task_1 = task_textboxes[0].get("1.0", END).strip().split('\n')
    user_agents_submitted = set([ua.strip() for ua in user_solution_task_1 if ua.strip()])
    if user_agents_submitted == user_agents:
        score += 20
        feedback.append("**Task 1:** Correct. You successfully listed all unique user agents.")
    else:
        partial_score = 10
        score += partial_score  # Partial credit
        missing_agents = user_agents - user_agents_submitted
        extra_agents = user_agents_submitted - user_agents
        feedback.append(f"**Task 1:** Partially correct.\n- Missing agents: {len(missing_agents)}\n- Extra agents not in log: {len(extra_agents)}")
    
    # Task 2 evaluation: Calculate percentage of 404 status codes
    with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as file:
        total_requests = 0
        status_404_count = 0
        for line in file:
            total_requests += 1
            status_code = re.search(r'\" (\d{3}) ', line)
            if status_code and status_code.group(1) == '404':
                status_404_count += 1
    percentage_404 = (status_404_count / total_requests) * 100 if total_requests > 0 else 0
    user_solution_task_2 = task_textboxes[1].get("1.0", END).strip().replace('%','')
    try:
        user_percentage_404 = float(user_solution_task_2)
        if abs(user_percentage_404 - percentage_404) < 0.1:
            score += 20
            feedback.append("**Task 2:** Correct. Your calculated percentage of 404 status codes is accurate.")
        else:
            partial_score = 10
            score += partial_score  # Partial credit
            feedback.append(f"**Task 2:** Partially correct.\n- Expected: {percentage_404:.2f}%\n- Your answer: {user_percentage_404}%")
    except ValueError:
        feedback.append("**Task 2:** Incorrect. Could not parse your percentage value.")
    
    # Task 3 evaluation: Identify top 5 most requested URLs
    with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as file:
        urls = re.findall(r'\"[A-Z]+ ([^ ]+) HTTP', file.read())
    url_counts = Counter(urls)
    top_5_urls = [url for url, count in url_counts.most_common(5)]
    user_solution_task_3 = task_textboxes[2].get("1.0", END).strip().split('\n')
    user_urls_submitted = [url.strip() for url in user_solution_task_3 if url.strip()]
    if user_urls_submitted == top_5_urls:
        score += 20
        feedback.append("**Task 3:** Correct. You correctly identified the top 5 most requested URLs.")
    else:
        partial_score = 10
        score += partial_score  # Partial credit
        missing_urls = set(top_5_urls) - set(user_urls_submitted)
        extra_urls = set(user_urls_submitted) - set(top_5_urls)
        feedback.append(f"**Task 3:** Partially correct.\n- Missing URLs: {len(missing_urls)}\n- Extra URLs not in top 5: {len(extra_urls)}")
    
    # Task 4 evaluation: Find the busiest hour
    with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as file:
        hours = []
        for line in file:
            timestamp_match = re.search(r'\[(\d{2})/[^:]+:(\d{2}):\d{2}:\d{2}', line)
            if timestamp_match:
                hour = timestamp_match.group(2)
                hours.append(hour)
    hour_counts = Counter(hours)
    busiest_hour = hour_counts.most_common(1)[0][0] if hour_counts else None
    user_solution_task_4 = task_textboxes[3].get("1.0", END).strip()
    if user_solution_task_4 == busiest_hour:
        score += 20
        feedback.append("**Task 4:** Correct. You correctly identified the busiest hour.")
    else:
        partial_score = 0
        score += partial_score
        feedback.append(f"**Task 4:** Incorrect.\n- Expected busiest hour: {busiest_hour}\n- Your answer: {user_solution_task_4}")
    
    # Task 5 evaluation: Determine average size of requests in bytes
    with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as file:
        sizes = []
        for line in file:
            size_match = re.search(r' (\d+)$', line.strip())
            if size_match:
                sizes.append(int(size_match.group(1)))
    average_size = sum(sizes) / len(sizes) if sizes else 0
    user_solution_task_5 = task_textboxes[4].get("1.0", END).strip()
    try:
        user_average_size = float(user_solution_task_5)
        if abs(user_average_size - average_size) < 1:
            score += 20
            feedback.append("**Task 5:** Correct. Your calculated average request size is accurate.")
        else:
            partial_score = 10
            score += partial_score  # Partial credit
            feedback.append(f"**Task 5:** Partially correct.\n- Expected: {average_size:.2f}\n- Your answer: {user_average_size}")
    except ValueError:
        feedback.append("**Task 5:** Incorrect. Could not parse your average size value.")
    
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
window = tb.Window(themename="cosmo")
window.title("Log File Analysis Exam")
window.geometry('1000x800')
window.resizable(True, True)
window.protocol("WM_DELETE_WINDOW", quit_application)

# Header frame
header_frame = Frame(window, bg="#283593")
header_frame.pack(fill=X)

header_label = tb.Label(
    header_frame, 
    text="Log File Analysis Exam", 
    font=("Helvetica", 24, "bold"), 
    anchor="center", 
    bootstyle="inverse"
)
header_label.pack(pady=20)

# Main frame with padding
main_frame = Frame(window, bg="#f0f0f0")
main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

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
