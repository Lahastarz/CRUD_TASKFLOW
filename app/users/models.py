import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from sqlalchemy import String, Boolean
from datetime import datetime 
from sqlalchemy import DateTime, func
from typing import TYPE_CHECKING
from sqlalchemy.orm import relationship


if TYPE_CHECKING:
    from app.tasks.models import Task

class User(Base):
    __tablename__ = "users"
     
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default= uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    tasks: Mapped[list["Task"]] = relationship(back_populates="owner", cascade="all, delete-orphan")
# The general Python rule this demonstrates

# function_name = "here's the function itself, call it later, whenever you need to."
# function_name() = "call it right now, and give me back whatever it returns."

# This exact mistake (default=uuid.uuid4() vs default=uuid.uuid4) is one of the most common subtle bugs in SQLAlchemy code — genuinely worth remembering.

# Does that distinction make sense now? If yes, go ahead and write the UUID-based id field yourself in your models.py, replacing the simple int version, and we'll add email next

print(User, User.__tablename__)