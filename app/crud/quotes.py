from sqlalchemy.orm import Session
from app.db import models
import random

def get_random_quote(db: Session):
    quotes = db.query(models.MotivationalQuote).all()
    if not quotes:
        return None
    return random.choice(quotes)
