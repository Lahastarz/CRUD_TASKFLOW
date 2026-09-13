import sqlalchemy
import asyncio
import asyncpg

def test_postgres_container_starts(postgres_container):
    connection_url = postgres_container.get_connection_url()
    print("Container connection URL:", connection_url)
    assert connection_url is not None

def test_migrations_create_tables(migrated_postgres):
    async def check():
        conn = await asyncpg.connect(migrated_postgres.replace("postgresql+asyncpg", "postgresql"))
        rows = await conn.fetch(
            "SELECT table_name FROM information_schema.tables WHERE table_schema='public'"
        )
        await conn.close()
        return {row["table_name"] for row in rows}

    tables = asyncio.run(check())
    print("Tables found:", tables)
    assert "users" in tables
    assert "tasks" in tables
    assert "alembic_version" in tables