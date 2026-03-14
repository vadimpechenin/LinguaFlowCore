import random

from sqlalchemy.orm import Session

from app.db.core.support.UUIDClass import UUIDClass
from app.db.models import Word, UserWordProgress


def create_word_by_data(db: Session, data) -> Word:
    ID = UUIDClass.geterateUUIDWithout_()
    word = Word(**data.dict())
    word.id = ID
    db.add(word)
    db.commit()
    db.refresh(word)
    return word


def list_words(db: Session, limit: int = 300):
    return db.query(Word).limit(limit).all()

def get_user_misssing_words(db: Session,userid, limit: int = 100):
    subquery = (
        db.query(UserWordProgress.wordid)
        .filter(UserWordProgress.userid == userid)
    )

    words = (
        db.query(Word)
        .filter(~Word.id.in_(subquery))
        .all()
    )
    selected = random.sample(words, min(limit, len(words)))

    return selected

def load_user_words(db: Session, user_id: str):
    #TODO надо заполнить сначала UserWordProgress тестово
    rows = db.query(Word.texten).join(
        UserWordProgress,
        Word.id == UserWordProgress.wordid
    ).filter(
        UserWordProgress.userid == user_id,
        UserWordProgress.isknown == True
    )
    rows = db.query(Word.texten)
    return set(row[0] for row in rows)

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