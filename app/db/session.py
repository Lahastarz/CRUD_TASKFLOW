from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from collections.abc import AsyncGenerator
engine = create_async_engine(str(settings.DATABASE_URL))
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_ = AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
        async with AsyncSessionLocal() as session:
                try:
                        yield session
                except Exception:
                        await session.rollback()
                        raise
                
                