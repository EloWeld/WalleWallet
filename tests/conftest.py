import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.database import get_db
from app.models import User

# Override the get_db dependency to use the regular database


def override_get_db():
    try:
        db = next(get_db())
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def db():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()
# Mock bot


class MockBot:
    async def send_message(self, chat_id, text, reply_markup=None):
        pass

    async def send_photo(self, chat_id, photo, caption=None, reply_markup=None):
        pass


@pytest.fixture
def mock_bot():
    return MockBot()
