from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.schemas import WalletBase
from app.db_repository import get_wallet


def test_create_wallet(client: TestClient, db: Session):
    response = client.post("/api/v1/wallets/", json={
        "wallet_id": 1,
        "user_id": 123456789,
        "currency_id": 1,
        "balance": 100.0
    })
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 123456789

    db_wallet = get_wallet(db, wallet_id=1)
    assert db_wallet
    assert db_wallet.user_id == 123456789


def test_read_wallets(client: TestClient):
    response = client.get("/api/v1/wallets/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


def test_read_user_wallets(client: TestClient):
    response = client.get("/api/v1/wallets/123456789")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


def test_wallet_not_found(client: TestClient):
    response = client.get("/api/v1/wallets/987654321")
    assert response.status_code == 404
