import pytest
from app.schemas import TaskCreate, TaskUpdate
import app.models as db

def setup_function():
    db.tasks_db.clear()
    db.current_id = 1

# Test création schema valide
def test_task_create_valid():
    task = TaskCreate(title="Ma tâche", priority="high")
    assert task.title == "Ma tâche"
    assert task.priority == "high"
    assert task.description is None

# Test schema invalide - titre vide
def test_task_create_empty_title():
    with pytest.raises(Exception):
        TaskCreate(title="", priority="medium")

# Test schema invalide - priorité incorrecte
def test_task_create_invalid_priority():
    with pytest.raises(Exception):
        TaskCreate(title="Test", priority="urgent")

# Test paramétré - priorités valides
@pytest.mark.parametrize("priority", ["low", "medium", "high"])
def test_task_create_all_priorities(priority):
    task = TaskCreate(title="Test", priority=priority)
    assert task.priority == priority

# Test paramétré - titres limites
@pytest.mark.parametrize("title,valid", [
    ("A", True),
    ("Titre normal", True),
    ("", False),
])
def test_task_title_validation(title, valid):
    if valid:
        task = TaskCreate(title=title)
        assert task.title == title
    else:
        with pytest.raises(Exception):
            TaskCreate(title=title)

# Test mock de la base de données
def test_task_added_to_db(monkeypatch):
    fake_db = []
    monkeypatch.setattr(db, "tasks_db", fake_db)
    monkeypatch.setattr(db, "current_id", 1)

    from app.routes import create_task
    task = TaskCreate(title="Mock task", priority="low")
    result = create_task(task)

    assert len(fake_db) == 1
    assert fake_db[0]["title"] == "Mock task"
    assert result["completed"] == False

# Test update schema optionnel
def test_task_update_partial():
    update = TaskUpdate(title="Nouveau titre")
    assert update.title == "Nouveau titre"
    assert update.priority is None
    assert update.completed is None