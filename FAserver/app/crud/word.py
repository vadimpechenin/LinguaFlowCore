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


def get_word_by_id(db: Session, word_id: str):
    return db.query(Word).get(word_id)

def list_words_duffuculty(db: Session,
                          difficulty: str | None = None,
                        limit: int = 20,
                        offset: int = 0):
    q = db.query(Word)
    if difficulty:
        q = q.filter(Word.difficulty_level == difficulty)
    return q.offset(offset).limit(limit).all()