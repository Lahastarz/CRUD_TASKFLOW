from sqlalchemy.ext.asyncio import AsyncSession
from app.tasks.models import Task
from app.tasks.schemas import TaskCreate, TaskUpdate
from sqlalchemy import select
from app.tasks.models import Task, TaskStatus


async def create_task(db: AsyncSession, owner_id: str, data: TaskCreate) -> Task:
    new_task = Task(
        owner_id = owner_id,
        title = data.title,
        description = data.description,
        due_date = data.due_date,
    )
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task

async def get_tasks_for_user(
        db: AsyncSession,
        owner_id: str,
        status_filter: TaskStatus | None = None,
) -> list[Task]:
    
    query = select(Task).where(Task.owner_id == owner_id)

    if status_filter is not None:
        query = query.where(Task.status == status_filter)

    result = await db.execute(query)
    return list(result.scalars().all())

async def get_task_by_id(db: AsyncSession, task_id: str, owner_id: str) -> Task|None:
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.owner_id==owner_id)
    )
    return result.scalar_one_or_none()

async def update_task(db: AsyncSession, task: Task, data: TaskUpdate) -> Task:
    if data.title is not None:
        task.title = data.title
    if data.description is not None:
        task.description = data.description

    if data.status is not None:
        task.status = data.status
    if data.due_date is not None:
        task.due_date = data.due_date

    await db.commit()
    await db.refresh(task)
    return task

async def delete_task(db: AsyncSession, task:Task)->None:
    await db.delete(task)
    await db.commit()