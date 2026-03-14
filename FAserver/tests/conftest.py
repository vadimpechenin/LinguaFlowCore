import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.api.deps import get_db
from app.services.ml_client import get_ml_client
from mocks.ml_client_mock import MockMLClient

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

@pytest.fixture()
def auth_headers(client):
    if (1==0):
        # создаём пользователя
        res = client.post(
            "/auth/register",
            json={"name": "Test",
                "username": "test_user_",
                "email": "test_user@example.com",
                "password": "password123",
                "initiallevel": "A2"},
        )
        assert res.status_code == 200

    res = client.post(
        "/auth/login",
        json={"username": "test_user_", "password": "password123"},
        #json={"username": "administrator", "password": "administrator"},
    )

    token = res.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}



@pytest.fixture(autouse=True)

def override_ml():
    app.dependency_overrides[get_ml_client] = (
        lambda: MockMLClient()
    )
    yield
    app.dependency_overrides.clear()



