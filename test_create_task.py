import asyncio
from app.db.session import AsyncSessionLocal
from app.auth.service import get_user_by_email
from app.tasks.service import create_task
from app.tasks.schemas import TaskCreate

async def main():
    async with AsyncSessionLocal() as db:
        user = await get_user_by_email(db, "test@example.com")
        print("User Found: ",user.id)

        task_data = TaskCreate(title="Finish Taskflow auth module", description="Wire up the router")
        task = await create_task(db, str(user.id), task_data)

        print("Created Task:")
        print("  id:", task.id)
        print("  owner_id:", task.owner_id)
        print("  title:", task.title)
        print("  status:", task.status)
        print("  created_at:", task.created_at)

asyncio.run(main())