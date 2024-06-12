from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import db_repository, schemas
from app.api import deps

router = APIRouter()


@router.get("/{user_id}", response_model=schemas.UserBase)
def read_user(user_id: int, db: Session = Depends(deps.get_db)):
    db_user = db_repository.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/", response_model=schemas.UserBase)
def create_user(user: schemas.UserBase, db: Session = Depends(deps.get_db)):
    return db_repository.create_user(db=db, user=user)
