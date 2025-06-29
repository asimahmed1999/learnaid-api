# app/api/routes/courses.py
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.models import Course
from app.db.session import SessionLocal
from app.db import schemas
from app.crud import courses as course_crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.CourseOut])
def list_courses(db: Session = Depends(get_db)):
    return course_crud.get_all_courses(db)


@router.get("/{course_id}/steps", response_model=list[schemas.ModuleOut])
def list_course_steps(course_id: UUID, db: Session = Depends(get_db)):
    steps = course_crud.get_course_steps(db, course_id)
    if not steps:
        return []

    # Convert each step object to dict, then rename 'image_url' to 'image'
    transformed_steps = []
    for step in steps:
        step_dict = step.__dict__.copy()
        step_dict["image"] = step_dict.pop("image_url", None)
        transformed_steps.append(step_dict)

    return transformed_steps


@router.get("/{course_id}/overview", response_model=schemas.CourseOverviewResponse)
def get_course_overview(course_id: str, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    sections = [
        schemas.CourseSection(
            icon=section.icon,
            image=section.image_url,
            highlight=section.highlight,
            title=section.title,
            text=section.text
        )
        for section in course.overview_sections
    ]

    return schemas.CourseOverviewResponse(
        id=str(course.id),
        title=course.title,
        subtitle=course.subtitle,
        description=course.description,
        sections=sections
    )