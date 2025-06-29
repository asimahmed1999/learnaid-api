from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional
from app.db.session import SessionLocal
from app.db import schemas
from app.crud import notes as notes_crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/users/{user_id}/notes", response_model=list[schemas.NoteOut])
def get_notes(user_id: UUID, course_id: Optional[UUID] = Query(None), db: Session = Depends(get_db)):
    return notes_crud.get_notes(db, user_id, course_id)

@router.post("/users/{user_id}/notes", response_model=schemas.NoteOut)
def create_note(user_id: UUID, note: schemas.NoteCreate, db: Session = Depends(get_db)):
    return notes_crud.create_note(db, user_id, note)
