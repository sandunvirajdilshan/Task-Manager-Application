import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_add_task_route(client):
    response = client.post('/addtask', data={
            'taskName': 'Test Task',
            'taskDescription': 'Test Description',
            'taskDate': '2024-02-22',
            'taskTime': '08:00'
    })
    assert response.status_code == 200
    assert b'true' in response.data

def test_get_tasks_route(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    assert b'true' in response.data
    tasks = response.json['tasks']
    global test_task_id
    test_task_id = tasks[0]['TaskId']

def test_edit_task_route(client):
    response = client.post('/edittask', data={
        'taskId': test_task_id,
        'taskName': 'Updated Task',
        'taskDescription': 'Updated Description',
        'taskDate': '2024-02-23',
        'taskTime': '09:00'
    })
    assert response.status_code == 200
    assert b'true' in response.data

def test_delete_task_route(client):
    response = client.delete('/deletetask', data={
        'taskId': test_task_id,
    })
    assert response.status_code == 200
    assert b'true' in response.data

if __name__ == "__main__":
    pytest.main()
