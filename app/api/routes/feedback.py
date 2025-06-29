from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.db import schemas
from app.db.session import SessionLocal
from app.crud import feedback as feedback_crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users/{user_id}/feedback")
def submit_feedback(user_id: UUID, feedback: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    return feedback_crud.submit_feedback(db, user_id, feedback)
