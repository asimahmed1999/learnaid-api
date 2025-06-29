# app/crud/courses.py

from sqlalchemy.orm import Session
from app.db import models
from uuid import UUID

def get_all_courses(db: Session):
    return db.query(models.Course).all()

def get_course_steps(db: Session, course_id: UUID) -> list[models.Module]:
    return (
        db.query(models.Module)
          .filter(models.Module.course_id == course_id)
          .order_by(models.Module.step_number)
          .all()
    )

