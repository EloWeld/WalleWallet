from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.schemas import UserBase
from app.db_repository import get_user


def test_create_user(client: TestClient, db: Session):
    response = client.post("/api/v1/users/", json={
        "user_id": 123456789,
        "username": "testuser",
        "full_name": "Test User",
        "avatar_file_id": "avatar_file_id"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"

    db_user = get_user(db, user_id=123456789)
    assert db_user
    assert db_user.username == "testuser"


def test_read_user(client: TestClient):
    response = client.get("/api/v1/users/123456789")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"


def test_user_not_found(client: TestClient):
    response = client.get("/api/v1/users/987654321")
    assert response.status_code == 404
