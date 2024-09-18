import sqlite3
from datetime import datetime, timedelta
from typing import Optional, List, Tuple
from flask import Flask, render_template, request, redirect, url_for
import matplotlib.pyplot as plt
import io
import base64
import random
from collections import defaultdict

app = Flask(__name__)

DATABASE_NAME = "study_tracker.db"
TABLE_NAME = "study_logs"

StudyLog = Tuple[int, str, str, Optional[int], Optional[str]]

class DatabaseManager:
    @staticmethod
    def create_database() -> None:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    duration INTEGER,
                    notes TEXT
                )
            """)

    @staticmethod
    def add_log(subject: str, duration: Optional[int] = None, notes: Optional[str] = None) -> None:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            date = datetime.now().strftime("%Y-%m-%d")
            cursor.execute(f"""
                INSERT INTO {TABLE_NAME} (date, subject, duration, notes)
                VALUES (?, ?, ?, ?)
            """, (date, subject, duration, notes))

    @staticmethod
    def view_logs() -> List[StudyLog]:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT * FROM {TABLE_NAME}
                ORDER BY date DESC, id DESC
            """)
            return cursor.fetchall()

    @staticmethod
    def delete_log(log_id: int) -> None:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE id = ?", (log_id,))

    @staticmethod
    def get_subjects() -> List[str]:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT DISTINCT subject FROM {TABLE_NAME}")
            return [row[0] for row in cursor.fetchall()]

def get_day_color(day: str) -> str:
    random.seed(day)  # Ensure the same day has the same color
    return "#%06x" % random.randint(0, 0xFFFFFF)

@app.route("/")
def index():
    logs = DatabaseManager.view_logs()
    colored_logs = [(log, get_day_color(log[1])) for log in logs]
    return render_template("index.html", logs=colored_logs)

@app.route("/add", methods=["GET", "POST"])
def add_log():
    if request.method == "POST":
        subject = request.form["subject"]
        duration = request.form["duration"]
        notes = request.form["notes"]
        if subject:
            try:
                duration = int(duration) if duration else None
                DatabaseManager.add_log(subject, duration, notes)
                return redirect(url_for("index"))
            except ValueError:
                return "Invalid duration. Please enter a number."
        else:
            return "Subject cannot be empty."
    subjects = DatabaseManager.get_subjects()
    return render_template("add_log.html", subjects=subjects)

@app.route("/delete/<int:log_id>")
def delete_log(log_id):
    DatabaseManager.delete_log(log_id)
    return redirect(url_for("index"))

@app.route("/statistics")
def view_statistics():
    logs = DatabaseManager.view_logs()
    if not logs:
        return "No logs found."

    subject_duration = defaultdict(int)
    dates = set()
    for log in logs:
        subject_duration[log[2]] += log[3] or 0
        dates.add(log[1])

    total_duration = sum(subject_duration.values())
    study_days = len(dates)
    average_duration = total_duration / study_days if study_days else 0

    plt.figure(figsize=(10, 7))
    plt.pie(subject_duration.values(), labels=subject_duration.keys(), autopct="%1.1f%%", startangle=90)
    plt.axis("equal")
    plt.title("Study Time Distribution by Subject")

    img = io.BytesIO()
    plt.savefig(img, format="png", facecolor='black', edgecolor='none')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode("utf8")

    return render_template("statistics.html", total_duration=total_duration, study_days=study_days, average_duration=average_duration, plot_url=plot_url)

if __name__ == "__main__":
    DatabaseManager.create_database()
    app.run(host="0.0.0.0", port=7777)
