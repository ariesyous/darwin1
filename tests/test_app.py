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


def test_delete_task():
    client = app.test_client()
    # Add task then delete it
    client.post('/add', data={'title': 'Task to Delete'}, follow_redirects=True)
    added = next((t for t in tasks if t['title'] == 'Task to Delete'), None)
    assert added is not None
    response = client.post(f'/delete/{added["id"]}', follow_redirects=True)
    assert response.status_code == 200
    assert not any(t['id'] == added['id'] for t in tasks)
    # Clean up
    tasks.clear()
    save_tasks()
