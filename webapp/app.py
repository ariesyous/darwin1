from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), 'tasks.json')

# Load tasks from disk if available
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
        tasks = json.load(f)
else:
    tasks = []


def save_tasks():
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f)


@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('title')
    if title:
        task = {
            'id': len(tasks) + 1,
            'title': title,
            'completed': False
        }
        tasks.append(task)
        save_tasks()
    return redirect(url_for('index'))


@app.route('/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = True
            break
    save_tasks()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
