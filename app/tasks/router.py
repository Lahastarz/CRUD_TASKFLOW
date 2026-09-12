from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies import get_current_user
from app.users.models import User
from app.tasks import service
from app.tasks.schemas import TaskResponse, TaskCreate, TaskUpdate
from app.tasks.models import TaskStatus
from fastapi import HTTPException

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model = list[TaskResponse])
async def list_tasks(
    status_filter: TaskStatus | None = Query(default=None, alias="status"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tasks = await service.get_tasks_for_user(db, str(current_user.id), status_filter)
    return tasks

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task_endpoint(
    body: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = await service.create_task(db, str(current_user.id), body)
    return task

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task_endpoint(
    task_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = await service.get_task_by_id(db, task_id, str(current_user.id))
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task Not Found")
    
    return task

@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task_endpoint(
    task_id: str,
    body: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = await service.get_task_by_id(db, task_id, str(current_user.id))
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task Not Found")
    
    updated_task = await service.update_task(db, task, body)
    return updated_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_endpoint(
    task_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = await service.get_task_by_id(db, task_id, str(current_user.id))
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task Not Found")
    await service.delete_task(db, task)