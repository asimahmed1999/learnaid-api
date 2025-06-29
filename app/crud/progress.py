from sqlalchemy.orm import Session
from sqlalchemy import func, asc
from app.db import models
from uuid import UUID
from datetime import datetime

from app.db.schemas import UserProgressResponse

def get_user_progress(db: Session, user_id: UUID, course_id: UUID) -> UserProgressResponse:
    # Check if user has any progress
    completed = (
        db.query(models.UserProgress.module_id)
        .filter(models.UserProgress.user_id == user_id)
        .filter(models.UserProgress.course_id == course_id)
        .filter(models.UserProgress.completed == True)
        .all()
    )
    completed_module_ids = [row[0] for row in completed]

    total_modules = (
        db.query(func.count(models.Module.id))
        .filter(models.Module.course_id == course_id)
        .scalar()
    )

    percent_complete = int((len(completed_module_ids) / total_modules) * 100) if total_modules else 0

    if completed_module_ids:
        current_module_id = completed_module_ids[-1]
    else:
        # No progress: fetch first module of the course
        first_module = (
            db.query(models.Module)
            .filter(models.Module.course_id == course_id)
            .order_by(asc(models.Module.step_number))  # or Module.id if no .order
            .first()
        )
        current_module_id = first_module.id if first_module else None

    return UserProgressResponse(
        current_module_id=current_module_id,
        completed_module_ids=completed_module_ids,
        percent_complete=percent_complete
    )


def update_user_progress(db: Session, user_id: UUID, course_id: UUID, current_module_id: UUID, completed_ids: list[UUID]):
    for module_id in completed_ids:
        exists = db.query(models.UserProgress).filter_by(
            user_id=user_id, course_id=course_id, module_id=module_id
        ).first()
        if not exists:
            progress = models.UserProgress(
                user_id=user_id,
                course_id=course_id,
                module_id=module_id,
                completed=True,
                completed_at=datetime.utcnow()
            )
            db.add(progress)
    db.commit()
    return {"success": True}
