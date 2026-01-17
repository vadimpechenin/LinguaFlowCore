from sqlalchemy.orm import Session

from app.db.core.support.UUIDClass import UUIDClass
from app.db.models import Word


def create_word(db: Session, data) -> Word:
    ID = UUIDClass.geterateUUIDWithout_()
    word = Word(**data.dict())
    word.id = ID
    db.add(word)
    db.commit()
    db.refresh(word)
    return word


def list_words(db: Session, limit: int = 300):
    return db.query(Word).limit(limit).all()