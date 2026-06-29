from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")
    due_date: Optional[date] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    priority: Optional[str] = Field(None, pattern="^(low|medium|high)$")
    due_date: Optional[date] = None
    completed: Optional[bool] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: str
    due_date: Optional[date]
    completed: bool