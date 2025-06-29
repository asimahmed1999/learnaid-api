from sqlalchemy import Column, String, DateTime, Text, JSON, ForeignKey, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100), nullable=True)
    avatar_url = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Course(Base):
    __tablename__ = "courses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    subtitle = Column(String(255))
    description = Column(Text)
    icon = Column(String(100))
    cover_image = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    overview_sections = relationship("CourseOverviewSection", back_populates="course", order_by="CourseOverviewSection.order")


class Module(Base):
    __tablename__ = "modules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    step_number = Column(Integer, nullable=False)
    type = Column(String(20), nullable=False)
    title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    image_url = Column(Text, nullable=True)
    options = Column(JSON, nullable=True)
    correct_answer = Column(String(255), nullable=True)
    explanation = Column(Text, nullable=True)
    
class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id", ondelete="CASCADE"))
    module_id = Column(UUID(as_uuid=True), ForeignKey("modules.id", ondelete="CASCADE"))
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, default=datetime.utcnow)
    reflection = Column(Text, nullable=True)
    confidence = Column(Integer, nullable=True)
    

class Note(Base):
    __tablename__ = "notes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id", ondelete="CASCADE"))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id", ondelete="CASCADE"))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class MotivationalQuote(Base):
    __tablename__ = "motivational_quotes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(Text, nullable=False)
    author = Column(String(100))

class CourseOverviewSection(Base):
    __tablename__ = "course_overview_sections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id", ondelete="CASCADE"))
    order = Column(Integer)
    icon = Column(String(50))
    title = Column(String(255))
    text = Column(Text, nullable=False)
    image_url = Column(Text)
    highlight = Column(Boolean, default=False)
    cta_label = Column(String(100))
    cta_action = Column(Text)

    course = relationship("Course", back_populates="overview_sections")