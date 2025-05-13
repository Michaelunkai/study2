import tkinter as tk
from tkinter import ttk, messagebox

questions = [
    {
        "question": "Which command in Bash ensures a script exits immediately if any command fails?",
        "options": ["set -x", "set -o pipefail", "set -e", "set -u"],
        "answer": "set -e",
        "explanation": "`set -e` exits a script immediately on any command failure, improving robustness in automation scripts."
    },
    {
        "question": "In Python, how do you run a command and capture both stdout and stderr?",
        "options": [
            "os.system('ls')",
            "subprocess.run(['ls'])",
            "subprocess.run(['ls'], capture_output=True, text=True)",
            "os.popen('ls')"
        ],
        "answer": "subprocess.run(['ls'], capture_output=True, text=True)",
        "explanation": "This is the correct way to capture both stdout and stderr while running commands securely in Python 3."
    },
    {
        "question": "Which tool best monitors system resource usage in real-time?",
        "options": ["df", "top", "ps", "du"],
        "answer": "top",
        "explanation": "`top` provides a live, real-time view of CPU, memory, and process usage."
    },
    {
        "question": "What does the 'chmod 750 file.sh' command do?",
        "options": [
            "Gives read, write, execute to owner; read+execute to group; none to others",
            "Only read+write for all",
            "Owner and group get all permissions",
            "Owner gets full; others get full"
        ],
        "answer": "Gives read, write, execute to owner; read+execute to group; none to others",
        "explanation": "750 means owner=rwx (7), group=rx (5), others=none (0)."
    },
    {
        "question": "What Python function checks if a file exists?",
        "options": ["os.file_exists()", "os.exists()", "os.path.isfile()", "os.check()"],
        "answer": "os.path.isfile()",
        "explanation": "`os.path.isfile(path)` returns True if the file exists and is a regular file."
    },
    {
        "question": "Which Bash snippet loops over all '.conf' files in /etc?",
        "options": [
            "for file in /etc/*.conf; do ...; done",
            "foreach file in /etc/*.conf { ... }",
            "loop /etc/*.conf as file { ... }",
            "for /etc/*.conf as file do ... done"
        ],
        "answer": "for file in /etc/*.conf; do ...; done",
        "explanation": "Standard Bash loop syntax for iterating over files with globbing."
    },
    {
        "question": "Which Linux command finds large files over 1GB in /home?",
        "options": [
            "du -ah /home | grep 1G",
            "find /home -size +1G",
            "find /home -type f -size +1G",
            "ls -lh /home | grep G"
        ],
        "answer": "find /home -type f -size +1G",
        "explanation": "Correct syntax to recursively find files larger than 1GB using `find`."
    },
    {
        "question": "In Bash, what does `>&2` mean?",
        "options": [
            "Redirects STDIN to STDERR",
            "Redirects STDOUT to STDERR",
            "Combines STDERR with STDOUT",
            "Silently suppresses all output"
        ],
        "answer": "Redirects STDOUT to STDERR",
        "explanation": "`>&2` redirects standard output (stdout) to standard error (stderr)."
    },
    {
        "question": "Which Python code lists all files in a directory?",
        "options": [
            "os.listdir(path)",
            "os.walk(path)",
            "glob.glob('*')",
            "shutil.listdir(path)"
        ],
        "answer": "os.listdir(path)",
        "explanation": "`os.listdir()` returns a list of names of the entries in the directory given by path."
    },
    {
        "question": "Which tool allows persistent background job scheduling on Linux?",
        "options": ["nohup", "watch", "cron", "ps"],
        "answer": "cron",
        "explanation": "`cron` is a daemon to schedule jobs at fixed times/dates repeatedly."
    }
]

class ExamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🧪 Advanced SysAdmin Exam")
        self.index = 0
        self.score = 0
        self.selected = tk.StringVar()

        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f4f8')
        self.style.configure('TLabel', font=('Segoe UI', 11), background='#f0f4f8')
        self.style.configure('TRadiobutton', font=('Segoe UI', 10), background='#f0f4f8')
        self.style.configure('TButton', font=('Segoe UI', 10, 'bold'))

        self.frame = ttk.Frame(root, padding=25)
        self.frame.pack(expand=True, fill="both")

        self.question_label = ttk.Label(self.frame, text="", wraplength=600, justify="left")
        self.question_label.pack(pady=(0, 20))

        self.radio_buttons = []
        for _ in range(4):
            btn = ttk.Radiobutton(self.frame, text="", variable=self.selected, value="")
            btn.pack(anchor="w", pady=5)
            self.radio_buttons.append(btn)

        self.feedback_label = ttk.Label(self.frame, text="", foreground="blue", wraplength=600)
        self.feedback_label.pack(pady=(10, 10))

        self.next_button = ttk.Button(self.frame, text="Submit", command=self.check_answer)
        self.next_button.pack(pady=15)

        self.show_question()

    def show_question(self):
        self.selected.set("")
        self.feedback_label.config(text="")
        q = questions[self.index]
        self.question_label.config(text=f"Q{self.index + 1} of {len(questions)}: {q['question']}")
        for i, option in enumerate(q['options']):
            self.radio_buttons[i].config(text=option, value=option)

    def check_answer(self):
        if not self.selected.get():
            messagebox.showwarning("Answer Required", "Please select an answer.")
            return

        current = questions[self.index]
        if self.selected.get() == current["answer"]:
            self.score += 1
            self.feedback_label.config(
                text=f"✅ Correct!\nExplanation: {current['explanation']}", foreground="green"
            )
        else:
            self.feedback_label.config(
                text=f"❌ Wrong.\nCorrect Answer: {current['answer']}\nExplanation: {current['explanation']}",
                foreground="red"
            )
        self.next_button.config(text="Next", command=self.next_question)

    def next_question(self):
        self.index += 1
        if self.index >= len(questions):
            self.show_result()
        else:
            self.show_question()
            self.next_button.config(text="Submit", command=self.check_answer)

    def show_result(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        result_text = f"🧾 Exam Completed!\n\nYour Score: {self.score} / {len(questions)}"
        ttk.Label(self.frame, text=result_text, font=("Segoe UI", 14)).pack(pady=40)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("700x500")
    app = ExamApp(root)
    root.mainloop()
