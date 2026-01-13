from sqlalchemy.orm import Session
from db.models import Word


def create_word(db: Session, data) -> Word:
    word = Word(**data.dict())
    db.add(word)
    db.commit()
    db.refresh(word)
    return word


def list_words(db: Session, limit: int = 100):
    return db.query(Word).limit(limit).all()