from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db import schemas
from app.crud import quotes as quote_crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/quotes/random", response_model=schemas.MotivationalQuoteOut)
def random_quote(db: Session = Depends(get_db)):
    quote = quote_crud.get_random_quote(db)
    if not quote:
        raise HTTPException(status_code=404, detail="No quotes found")
    return quote
