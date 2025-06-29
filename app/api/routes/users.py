from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.session import SessionLocal
from app.db import schemas
from app.crud import users as user_crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/users/{user_id}", response_model=schemas.UserProfileOut)
def get_user_profile(user_id: UUID, db: Session = Depends(get_db)):
    return user_crud.get_user_profile(db, user_id)

@router.put("/users/{user_id}", response_model=schemas.UserProfileOut)
def update_user_profile(user_id: UUID, update: schemas.UserProfileUpdate, db: Session = Depends(get_db)):
    return user_crud.update_user_profile(db, user_id, update)
