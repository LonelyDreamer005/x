import pytest
from app import app, students

@pytest.fixture(autouse=True)
def reset_students():
    """Reset the students list to known state before each test."""
    students.clear()
    students.extend([
        {"id": 1, "name": "Rahul", "age": 20, "department": "CSE"},
        {"id": 2, "name": "Priya", "age": 21, "department": "CSE"}
    ])

def test_home():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert "DevOps Student REST API" in response.json["message"]

def test_health():
    client = app.test_client()
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json["status"] == "UP"

def test_get_students():
    client = app.test_client()
    response = client.get('/students')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) == 2

def test_get_single_student():
    client = app.test_client()
    response = client.get('/students/1')
    assert response.status_code == 200
    assert response.json["name"] == "Rahul"
    assert response.json["department"] == "CSE"

def test_add_student():
    client = app.test_client()
    response = client.post('/students', json={
        "name": "Kiran",
        "age": 20,
        "department": "CSE"
    })
    assert response.status_code == 201
    assert response.json["name"] == "Kiran"
    assert response.json["id"] == 3

def test_update_student():
    client = app.test_client()
    response = client.put('/students/1', json={
        "name": "Rahul Sharma",
        "age": 21
    })
    assert response.status_code == 200
    assert response.json["name"] == "Rahul Sharma"
    assert response.json["age"] == 21

def test_delete_student():
    client = app.test_client()
    response = client.delete('/students/1')
    assert response.status_code == 200
    assert response.json["message"] == "Deleted successfully"

    # Verify student is removed
    verify_res = client.get('/students/1')
    assert verify_res.status_code == 404

def test_invalid_student():
    client = app.test_client()
    response = client.get('/students/9999')
    assert response.status_code == 404
    assert response.json["message"] == "Not found"
