import pytest
import pytest_asyncio
from testcontainers.postgres import PostgresContainer
# from testcontainers.community.postgres import PostgresContainer
import subprocess
import os
import uuid
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db.session import get_db
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.middleware.rate_limit import limiter

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

@pytest_asyncio.fixture
async def client(migrated_postgres):
    test_engine = create_async_engine(migrated_postgres)
    TestSessionLocal = async_sessionmaker(bind=test_engine, expire_on_commit=False)

    async def override_get_db():
        async with TestSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
    await test_engine.dispose()


@pytest.fixture(autouse=True)
def disable_rate_limit():
    limiter.enabled=False
    yield
    limiter.enabled=True

@pytest.fixture
def make_headers(client):
    async def _make(email=None, password="Pass123!"):
        email=email or f"user-{uuid.uuid4().hex[:8]}@example.com"
        await client.post("/auth/register", json={"email":email, "password":password})
        login=await client.post("/auth/login", json={"email":email, "password":password})
        return {"Authorization":f"Bearer {login.json()['access_token']}"}
    return _make

@pytest_asyncio.fixture
async def auth_headers(make_headers):
    return await make_headers()