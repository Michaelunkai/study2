import sys
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
    QRadioButton, QPushButton, QButtonGroup, QMessageBox,
    QFrame, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtCore import Qt

questions = [
    {
        "question": "Which command restarts the NetworkManager service on systemd-based Linux?",
        "options": ["systemctl start networking", "systemctl restart NetworkManager", "service network restart", "nmcli reload"],
        "answer": "systemctl restart NetworkManager",
        "explanation": "Use 'systemctl restart NetworkManager' on systemd systems to reload and restart network configurations."
    },
    {
        "question": "What is the default SSH port?",
        "options": ["21", "80", "22", "443"],
        "answer": "22",
        "explanation": "SSH by default communicates over port 22 unless otherwise specified."
    },
    {
        "question": "Which file holds user account info in Linux?",
        "options": ["/etc/shadow", "/etc/group", "/etc/users", "/etc/passwd"],
        "answer": "/etc/passwd",
        "explanation": "The /etc/passwd file holds user account information like usernames and default shells."
    },
    {
        "question": "How do you see open TCP connections?",
        "options": ["ss -t", "netstat -l", "ping -t", "ip a"],
        "answer": "ss -t",
        "explanation": "The 'ss -t' command shows current TCP connections with better performance than netstat."
    },
    {
        "question": "Which tool monitors logs in real time?",
        "options": ["less /var/log/syslog", "tail -f /var/log/syslog", "cat /var/log/syslog", "logrotate"],
        "answer": "tail -f /var/log/syslog",
        "explanation": "'tail -f' is used for live monitoring of logs as new lines are written."
    },
    {
        "question": "Which command changes a user’s primary group?",
        "options": ["usermod -g group user", "groupmod user group", "chown group user", "setgid group user"],
        "answer": "usermod -g group user",
        "explanation": "To change a user's primary group, use 'usermod -g group user'."
    },
    {
        "question": "What does 'df -h' display?",
        "options": ["Network interfaces", "Free and used memory", "Disk usage in human-readable format", "Mounted devices only"],
        "answer": "Disk usage in human-readable format",
        "explanation": "'df -h' gives disk usage in readable format like GB and MB."
    },
    {
        "question": "How to give a script execute permission?",
        "options": ["chmod +r script.sh", "chmod +x script.sh", "chown +x script.sh", "exec script.sh"],
        "answer": "chmod +x script.sh",
        "explanation": "'chmod +x script.sh' gives the execute permission to run the script."
    },
    {
        "question": "Which command shows real-time system resource stats?",
        "options": ["top", "df", "uptime", "env"],
        "answer": "top",
        "explanation": "'top' gives a live updating list of resource usage and running processes."
    },
    {
        "question": "How to schedule a cron job every 5 minutes?",
        "options": ["*/5 * * * *", "0/5 * * * *", "* * * * */5", "5/0 * * * *"],
        "answer": "*/5 * * * *",
        "explanation": "The crontab expression '*/5 * * * *' means every 5 minutes."
    }
]

class SysAdminExam(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧠 SysAdmin Scripting Exam")
        self.setGeometry(300, 100, 900, 640)

        self.index = 0
        self.score = 0

        if os.path.exists("lobster.ttf"):
            QFontDatabase.addApplicationFont("lobster.ttf")
        self.setFont(QFont("Lobster", 13))

        self.setStyleSheet("""
            QWidget {
                background-color: #0f111a;
                color: #eaeaea;
                font-size: 15px;
            }
            QLabel {
                color: #f2f2f2;
            }
            QRadioButton {
                padding: 8px;
                font-size: 15px;
            }
            QPushButton {
                background-color: #03a9f4;
                color: white;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0288d1;
            }
        """)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        header = QLabel("💻 System Administrator Certification - Practice Exam")
        header.setFont(QFont("Lobster", 22))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: cyan;")
        self.layout.addWidget(header)

        self.divider = QFrame()
        self.divider.setFrameShape(QFrame.HLine)
        self.divider.setStyleSheet("color: #444;")
        self.layout.addWidget(self.divider)

        self.question_label = QLabel()
        self.question_label.setWordWrap(True)
        self.layout.addWidget(self.question_label)

        self.options_group = QButtonGroup()
        self.option_buttons = []
        for _ in range(4):
            btn = QRadioButton()
            self.layout.addWidget(btn)
            self.options_group.addButton(btn)
            self.option_buttons.append(btn)

        self.feedback_label = QLabel("")
        self.feedback_label.setWordWrap(True)
        self.layout.addWidget(self.feedback_label)

        self.button_layout = QHBoxLayout()
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.check_answer)
        self.button_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.button_layout.addWidget(self.submit_button)
        self.button_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.layout.addLayout(self.button_layout)

        self.show_question()

    def show_question(self):
        self.options_group.setExclusive(False)
        for btn in self.option_buttons:
            btn.setChecked(False)
        self.options_group.setExclusive(True)

        current = questions[self.index]
        self.question_label.setText(f"<b>Q{self.index + 1}:</b> {current['question']}")
        for i, option in enumerate(current["options"]):
            self.option_buttons[i].setText(option)

        self.feedback_label.setText("")
        self.submit_button.setText("Submit")
        self.submit_button.clicked.disconnect()
        self.submit_button.clicked.connect(self.check_answer)

    def check_answer(self):
        selected = next((btn.text() for btn in self.option_buttons if btn.isChecked()), None)
        if not selected:
            QMessageBox.warning(self, "No selection", "Please select an answer to continue.")
            return

        correct = questions[self.index]["answer"]
        explanation = questions[self.index]["explanation"]

        if selected == correct:
            self.score += 1
            self.feedback_label.setStyleSheet("color: lightgreen;")
            self.feedback_label.setText(f"✅ Correct!\n{explanation}")
        else:
            self.feedback_label.setStyleSheet("color: tomato;")
            self.feedback_label.setText(f"❌ Incorrect.\n<b>Correct answer:</b> {correct}\n{explanation}")

        self.submit_button.setText("Next")
        self.submit_button.clicked.disconnect()
        self.submit_button.clicked.connect(self.next_question)

    def next_question(self):
        self.index += 1
        if self.index >= len(questions):
            self.display_results()
        else:
            self.show_question()

    def display_results(self):
        for widget in self.findChildren(QWidget):
            widget.hide()

        result = QLabel(f"🎉 Exam Completed!\n\nFinal Score: {self.score} / {len(questions)}")
        result.setFont(QFont("Lobster", 24))
        result.setAlignment(Qt.AlignCenter)
        result.setStyleSheet("color: cyan;")
        self.layout.addWidget(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    exam = SysAdminExam()
    exam.show()
    sys.exit(app.exec())
