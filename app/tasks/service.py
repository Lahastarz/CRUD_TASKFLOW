from sqlalchemy.ext.asyncio import AsyncSession
from app.tasks.models import Task
from app.tasks.schemas import TaskCreate

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
