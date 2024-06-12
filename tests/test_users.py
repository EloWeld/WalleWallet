from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.schemas import UserBase
from app.db_repository import get_user

TEST_USER_TGID = 123456789


def test_create_user(client: TestClient, db: Session):
    existing_user = get_user(db, user_id=TEST_USER_TGID)

    if existing_user:
        # Optionally, you can delete the existing user for test isolation
        db.delete(existing_user)
        db.commit()
    response = client.post("/api/v1/users/", json={
        "user_id": TEST_USER_TGID,
        "username": "testuser",
        "full_name": "Test User",
        "avatar_file_id": "avatar_file_id"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"

    db_user = get_user(db, user_id=TEST_USER_TGID)
    assert db_user
    assert db_user.username == "testuser"


def test_read_user(client: TestClient):
    response = client.get(f"/api/v1/users/{TEST_USER_TGID}")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"


def test_user_not_found(client: TestClient):
    response = client.get("/api/v1/users/000000")
    assert response.status_code == 404
