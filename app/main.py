# app/main.py
from fastapi import FastAPI
from app.api.routes import auth, users, progress, courses, notes, feedback, quotes  # import the route module

app = FastAPI(title="LearnAid API")

# Include the /auth routes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(courses.router, prefix="/courses", tags=["Courses"])
app.include_router(progress.router, tags=["Progress"])
app.include_router(users.router, tags=["Users"])
app.include_router(notes.router, tags=["Notes"])
app.include_router(feedback.router, tags=["Feedback"])
app.include_router(quotes.router, tags=["Quotes"])