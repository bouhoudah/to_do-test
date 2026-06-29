from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.schemas import TaskCreate, TaskUpdate, TaskResponse
import app.models as db

router = APIRouter()

@router.get("/tasks", response_model=List[TaskResponse])
def get_tasks(completed: Optional[bool] = None, priority: Optional[str] = None):
    tasks = db.tasks_db
    if completed is not None:
        tasks = [t for t in tasks if t["completed"] == completed]
    if priority is not None:
        tasks = [t for t in tasks if t["priority"] == priority]
    return tasks

@router.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate):
    new_task = {
        "id": db.current_id,
        "title": task.title,
        "description": task.description,
        "priority": task.priority,
        "due_date": task.due_date,
        "completed": False
    }
    db.tasks_db.append(new_task)
    db.current_id += 1
    return new_task

@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    for task in db.tasks_db:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, updates: TaskUpdate):
    for task in db.tasks_db:
        if task["id"] == task_id:
            if updates.title is not None:
                task["title"] = updates.title
            if updates.description is not None:
                task["description"] = updates.description
            if updates.priority is not None:
                task["priority"] = updates.priority
            if updates.due_date is not None:
                task["due_date"] = updates.due_date
            if updates.completed is not None:
                task["completed"] = updates.completed
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for i, task in enumerate(db.tasks_db):
        if task["id"] == task_id:
            db.tasks_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="Task not found")