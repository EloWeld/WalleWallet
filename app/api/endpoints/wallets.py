from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import db_repository, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=list[schemas.WalletBase])
def read_wallets(skip: int = 0, limit: int = 10, db: Session = Depends(deps.get_db)):
    wallets = db_repository.get_wallets(db, skip=skip, limit=limit)
    return wallets


@router.get("/{user_id}", response_model=list[schemas.WalletBase])
def read_wallets(user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(deps.get_db)):
    user = db_repository.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    wallets = db_repository.get_user_wallets(db, user.id, skip=skip, limit=limit)
    return wallets


@router.post("/", response_model=schemas.WalletBase)
def create_wallet(wallet: schemas.WalletBase, db: Session = Depends(deps.get_db)):
    return db_repository.create_wallet(db=db, wallet=wallet)
