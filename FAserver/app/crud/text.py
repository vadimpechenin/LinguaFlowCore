from typing import Dict

from sqlalchemy.orm import Session

from app.db.core.support.UUIDClass import UUIDClass
from app.db.models import Text, User, TextVocabularyStats
from app.schemas.text import TextRequest


def create_text(db: Session, user: User, data: TextRequest, result_of_analize: Dict) -> Text:
    #Операция подсчета слов и охвата текста
    ID = UUIDClass.geterateUUIDWithout_()
    text = Text(**data.dict())
    text.id = ID
    text.userid= user.id
    text.user = user
    # Сначала создаем vocabularystats
    vocStats = TextVocabularyStats( id = UUIDClass.geterateUUIDWithout_(),
        textid = text.id,
        totalwords = result_of_analize['total_words'],
        knownwords = result_of_analize['known_words'],
        unknownwords = result_of_analize['unknown_words'],
        coveragepercent = result_of_analize['coverage_percent'])
    text.vocabularystats = vocStats
    vocStats.text = text
    db.add(vocStats)
    db.add(text)
    db.commit()
    db.refresh(text)
    return text


def get_text_by_title(db: Session, title: str, userid: str) -> Text | None:
    return db.query(Text).filter(Text.title == title, Text.userid == userid).first()


