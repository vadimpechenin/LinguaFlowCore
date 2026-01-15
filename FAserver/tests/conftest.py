import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.api.deps import get_db
from app.db.core.base import Base

TEST_DATABASE_URL = "postgresql+psycopg2://postgres:mapr@localhost:5432/lfc"

engine = create_engine(
    TEST_DATABASE_URL,
    pool_pre_ping=True,
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


def override_get_db():
    session = TestingSessionLocal()
    try:
        yield session
        session.commit()
    finally:
        session.close()


"""
@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
"""

@pytest.fixture()
def client():
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)
