from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.db import schemas
from app.db.session import SessionLocal
from app.crud import progress as progress_crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/users/{user_id}/courses/{course_id}/progress", response_model=schemas.UserProgressResponse)
def get_progress(user_id: UUID, course_id: UUID, db: Session = Depends(get_db)):
    return progress_crud.get_user_progress(db, user_id, course_id)

@router.post("/users/{user_id}/courses/{course_id}/progress")
def update_progress(user_id: UUID, course_id: UUID, body: schemas.UserProgressUpdate, db: Session = Depends(get_db)):
    return progress_crud.update_user_progress(db, user_id, course_id, body.current_module_id, body.completed_module_ids)
