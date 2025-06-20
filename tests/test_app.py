import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
from webapp.app import app, tasks, save_tasks


def test_index_route():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200


def test_add_task():
    client = app.test_client()
    response = client.post('/add', data={'title': 'Test Task'}, follow_redirects=True)
    assert response.status_code == 200
    assert any(t['title'] == 'Test Task' for t in tasks)
    # Clean up
    tasks.clear()
    save_tasks()
