from sqlalchemy.orm import Session
from app.db import models, schemas
from uuid import UUID
from fastapi import HTTPException

def get_user_profile(db: Session, user_id: UUID):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def update_user_profile(db: Session, user_id: UUID, update_data: schemas.UserProfileUpdate):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if update_data.name is not None:
        user.name = update_data.name
    if update_data.avatar_url is not None:
        user.avatar_url = update_data.avatar_url

    db.commit()
    db.refresh(user)
    return user
