# app/crud/auth.py
from sqlalchemy.orm import Session
from app.db import models, schemas
from app.core.security import hash_password, verify_password, create_access_token
from fastapi import HTTPException, status
from datetime import timedelta
from app.core.config import settings


def register_user(db: Session, user_data: schemas.UserCreate) -> schemas.UserOut:
    existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    user = models.User(
        email=user_data.email,
        name=user_data.name,
        password_hash=hash_password(user_data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(data={"sub": str(user.id)}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    return {
        "user": schemas.UserOut.from_orm(user),
        "token": token,
        "refreshToken": "not_implemented_yet"
    }
