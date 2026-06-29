import pytest
from fastapi.testclient import TestClient
from app.main import app
import app.models as db

client = TestClient(app)

def setup_function():
    db.tasks_db.clear()
    db.current_id = 1

# GET /tasks - liste vide
def test_get_tasks_empty():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []

# POST /tasks - création réussie
def test_create_task():
    response = client.post("/tasks", json={"title": "Acheter du lait", "priority": "low"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Acheter du lait"
    assert data["completed"] == False
    assert data["id"] == 1

# POST /tasks - titre vide → 422
def test_create_task_invalid_title():
    response = client.post("/tasks", json={"title": "", "priority": "medium"})
    assert response.status_code == 422

# POST /tasks - priorité invalide → 422
def test_create_task_invalid_priority():
    response = client.post("/tasks", json={"title": "Test", "priority": "urgent"})
    assert response.status_code == 422

# GET /tasks/{id} - tâche existante
def test_get_task_by_id():
    client.post("/tasks", json={"title": "Tâche 1", "priority": "high"})
    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert response.json()["title"] == "Tâche 1"

# GET /tasks/{id} - tâche inexistante → 404
def test_get_task_not_found():
    response = client.get("/tasks/999")
    assert response.status_code == 404

# PUT /tasks/{id} - mise à jour réussie
def test_update_task():
    client.post("/tasks", json={"title": "Ancienne tâche", "priority": "low"})
    response = client.put("/tasks/1", json={"title": "Nouvelle tâche", "completed": True})
    assert response.status_code == 200
    assert response.json()["title"] == "Nouvelle tâche"
    assert response.json()["completed"] == True

# PUT /tasks/{id} - tâche inexistante → 404
def test_update_task_not_found():
    response = client.put("/tasks/999", json={"title": "Test"})
    assert response.status_code == 404

# DELETE /tasks/{id} - suppression réussie
def test_delete_task():
    client.post("/tasks", json={"title": "A supprimer", "priority": "medium"})
    response = client.delete("/tasks/1")
    assert response.status_code == 204

# DELETE /tasks/{id} - tâche inexistante → 404
def test_delete_task_not_found():
    response = client.delete("/tasks/999")
    assert response.status_code == 404

# GET /tasks?completed=false - filtre
def test_filter_by_completed():
    client.post("/tasks", json={"title": "Tâche 1", "priority": "low"})
    client.post("/tasks", json={"title": "Tâche 2", "priority": "high"})
    client.put("/tasks/1", json={"completed": True})
    response = client.get("/tasks?completed=false")
    assert response.status_code == 200
    assert len(response.json()) == 1

# GET /tasks?priority=high - filtre priorité
def test_filter_by_priority():
    client.post("/tasks", json={"title": "Tâche high", "priority": "high"})
    client.post("/tasks", json={"title": "Tâche low", "priority": "low"})
    response = client.get("/tasks?priority=high")
    assert response.status_code == 200
    assert all(t["priority"] == "high" for t in response.json())