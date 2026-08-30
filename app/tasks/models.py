import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from sqlalchemy import String, Text, DateTime, func
from sqlalchemy import Enum as SAEnum
from datetime import datetime
from sqlalchemy import Index
from typing import TYPE_CHECKING
from sqlalchemy.orm import relationship
import enum 
class TaskStatus(str, enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

if TYPE_CHECKING:
    from app.users.models import User


class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = (Index("ix_tasks_owner_id_status", "owner_id", "status"),)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(
        SAEnum(TaskStatus, name = "task_status", native_enum=True),
        default=TaskStatus.TODO,
        nullable=False,
    )
    due_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    owner: Mapped["User"] = relationship(back_populates="tasks")

print(Task, Task.__tablename__)
print(Task.owner_id.type)