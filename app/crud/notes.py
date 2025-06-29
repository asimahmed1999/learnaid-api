from sqlalchemy.orm import Session
from app.db import models, schemas
from uuid import UUID
from datetime import datetime

def get_notes(db: Session, user_id: UUID, course_id: UUID = None):
    query = db.query(models.Note).filter(models.Note.user_id == user_id)
    if course_id:
        query = query.filter(models.Note.course_id == course_id)
    return query.order_by(models.Note.created_at.desc()).all()

def create_note(db: Session, user_id: UUID, note_data: schemas.NoteCreate):
    note = models.Note(
        user_id=user_id,
        course_id=note_data.course_id,
        content=note_data.content,
        created_at=datetime.utcnow()
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note
