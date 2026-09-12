from pydantic import BaseModel
from datetime import datetime
from app.tasks.models import TaskStatus
import uuid

class TaskCreate(BaseModel):
    title: str|None = None
    description: str|None = None
    due_date: datetime|None = None


class TaskUpdate(BaseModel):
    title: str|None = None
    description: str|None = None
    due_date: datetime|None = None
    status: TaskStatus|None = None

class TaskResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str|None
    status: TaskStatus
    due_date: datetime|None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes":True}



