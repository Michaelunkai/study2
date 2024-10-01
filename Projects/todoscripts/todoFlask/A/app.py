from flask import Flask, render_template, request, redirect, url_for
from urllib.parse import unquote
import os

app = Flask(__name__)

TASKS_FILE = 'tasks.txt'

class Task:
    def __init__(self, name, category):
        self.name = name
        self.category = category

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as file:
            tasks = [line.strip().split(' - ') for line in file.readlines()]
            return [Task(name, category) for name, category in tasks]
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        for task in tasks:
            file.write(f'{task.name} - {task.category}\n')

@app.route('/', methods=['GET', 'POST'])
def index():
    selected_category = request.form.get('category', 'all')

    if request.method == 'POST':
        new_task = request.form.get('task')
        new_category = request.form.get('category')
        tasks = load_tasks()
        tasks.append(Task(new_task, new_category))
        save_tasks(tasks)

    tasks = load_tasks()
    categories = set(task.category for task in tasks)

    # Filter tasks based on the selected category
    if selected_category != 'all':
        tasks = [task for task in tasks if task.category == selected_category]

    return render_template('index.html', tasks=tasks, categories=categories, current_category=selected_category)

@app.route('/delete/<task>', methods=['POST'])
def delete_task(task):
    decoded_task = unquote(task)  # URL decode the task name
    tasks = load_tasks()
    tasks = [t for t in tasks if t.name != decoded_task]
    save_tasks(tasks)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
