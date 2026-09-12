import pytest
import pytest_asyncio
from testcontainers.postgres import PostgresContainer
from testcontainers.community.postgres import PostgresContainer

@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:16-alpine") as container:
        yield container