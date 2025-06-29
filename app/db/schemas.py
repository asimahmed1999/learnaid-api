from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from uuid import UUID  # Add this at the top

# ✅ Used for incoming registration data
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str


class UserOut(BaseModel):
    id: UUID  # <- change from str to UUID
    email: EmailStr
    name: str
    avatar_url: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # ✅ Pydantic v2 requirement


# ✅ Used for login endpoint
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# ✅ Response wrapper: user info + token
class TokenResponse(BaseModel):
    user: UserOut
    token: str
    refreshToken: str  # Placeholder
    

class CourseOut(BaseModel):
    id: UUID
    title: str
    subtitle: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    cover_image: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
        
class ModuleOut(BaseModel):
    id: UUID
    step_number: int
    type: str
    title: Optional[str]
    description: Optional[str]
    image: Optional[str]
    options: Optional[list]        # will decode JSONB
    correct_answer: Optional[str]
    explanation: Optional[str]

    class Config:
        from_attributes = True


class UserProgressGet(BaseModel):
    current_module_id: UUID
    completed_module_ids: list[UUID]
    percent_complete: int

class UserProgressUpdate(BaseModel):
    current_module_id: UUID
    completed_module_ids: list[UUID]

class UserProfileOut(BaseModel):
    id: UUID
    email: EmailStr
    name: Optional[str]
    avatar_url: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    
class NoteCreate(BaseModel):
    course_id: UUID
    content: str

class NoteOut(BaseModel):
    id: UUID
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

class FeedbackCreate(BaseModel):
    course_id: UUID
    content: str

class MotivationalQuoteOut(BaseModel):
    content: str
    author: Optional[str] = None

    class Config:
        from_attributes = True


class CourseSection(BaseModel):
    icon: Optional[str]
    image: any
    highlight: Optional[bool] = False
    title: Optional[str]
    text: str


class CourseOverviewResponse(BaseModel):
    id: str
    title: str
    subtitle: str
    description: str
    sections: List[CourseSection]
    
class UserProgressResponse(BaseModel):
    current_module_id: Optional[UUID]
    completed_module_ids: List[UUID]
    percent_complete: int