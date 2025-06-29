from sqlalchemy.orm import Session
from app.db import models, schemas
from uuid import UUID
from datetime import datetime

def submit_feedback(db: Session, user_id: UUID, feedback_data: schemas.FeedbackCreate):
    feedback = models.Feedback(
        user_id=user_id,
        course_id=feedback_data.course_id,
        content=feedback_data.content,
        created_at=datetime.utcnow()
    )
    db.add(feedback)
    db.commit()
    return {"success": True}
