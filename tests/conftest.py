import pytest
import pytest_asyncio
from testcontainers.postgres import PostgresContainer
# from testcontainers.community.postgres import PostgresContainer
import subprocess
import os

@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:16-alpine") as container:
        yield container

@pytest.fixture(scope="session")
def migrated_postgres(postgres_container):
    db_url = postgres_container.get_connection_url().replace("psycopg2","asyncpg")
    env = os.environ.copy()
    env['DATABASE_URL'] = db_url
    subprocess.run(["alembic","upgrade", "head"], env=env, check=True)

    return db_url