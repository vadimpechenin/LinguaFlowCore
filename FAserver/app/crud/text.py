from sqlalchemy.orm import Session

from app.crud.word import load_user_words
from app.db.core.support.UUIDClass import UUIDClass
from app.db.models import Text, User, TextVocabularyStats


def create_text(db: Session, user: User, data) -> Text:
    #Операция подсчета слов и охвата текста
    user_words =load_user_words(db, user.id)
    analyzer = TextCoverageAnalyzer(user_words)

    result = analyzer.analyze(data.content)
    ID = UUIDClass.geterateUUIDWithout_()
    text = Text(**data.dict())
    text.id = ID
    text.userid= user.id
    text.user = user
    # Сначала создаем vocabularystats
    vocStats = TextVocabularyStats( id = UUIDClass.geterateUUIDWithout_(),
        textid = text.id,
        totalwords = result['total_words'],
        knownwords = result['known_words'],
        unknownwords = result['unknown_words'],
        coveragepercent = result['coverage_percent'])
    text.vocabularystats = vocStats
    vocStats.text = text
    db.add(vocStats)
    db.add(text)
    db.commit()
    db.refresh(text)
    return text


def get_text_by_title(db: Session, title: str, userid: str) -> Text | None:
    return db.query(Text).filter(Text.title == title, Text.userid == userid).first()


import re
from typing import Set, Dict
import spacy

nlp = spacy.load("en_core_web_sm")

class TextCoverageAnalyzer:

    def __init__(self, user_words: Set[str]):
        # приводим к lowercase
        self.user_words = set(
            word.lower()
            for word in user_words
        )

    def preprocess_text(
            self,
            text: str
    ) -> Set[str]:
        # извлекаем только слова - базовая версия
        words = re.findall(
            r"[a-zA-Z']+",
            text.lower()

        )
        return set(words)

    def preprocess_text_nlp(self,text):
        #Улучшенная версия
        # с лемматизацией; частотным анализом
        doc = nlp(text)

        return set(
            token.lemma_
            for token in doc
            if token.is_alpha
        )

    def analyze(
            self,
            text: str
        ) -> Dict:
        #text_words = self.preprocess_text(text)
        text_words = self.preprocess_text_nlp(text)

        known = text_words.intersection(
            self.user_words
        )

        unknown = text_words.difference(
            self.user_words
        )

        total = len(text_words)
        known_count = len(known)
        unknown_count = len(unknown)

        coverage = (
            known_count / total * 100
            if total > 0 else 0
        )

        return {
            "total_words": total,
            "known_words": known_count,
            "unknown_words": unknown_count,
            "coverage_percent": round(coverage, 2),
            "unknown_words_list": sorted(list(unknown))
        }