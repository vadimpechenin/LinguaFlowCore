import re
import spacy
from typing import Dict, Set

from app.services.pipelines.word_analyzer import WordAnalyzer

nlp = spacy.load("en_core_web_sm")

class TextAnalyzer:
    """
    Text
    ↓
    Tokenizer
    ↓
    BERT encoder
    ↓
    CEFR classifier
    ↓
    Recommendation engine
    ↓
    Response
    """
    def __init__(self, user_words: Set[str]):
        # приводим к lowercase
        self.user_words = set(
            word.lower()
            for word in user_words
        )
        self.word_analyzer = WordAnalyzer()


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
        #Уровни сложности слов, пока не используем
        #result = self.word_analyzer.analyze(list(text_words))
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
        #Оценка сложности текста
        dif_res = self.word_analyzer.dif_predictor(list(unknown))

        if dif_res < 0.15:
            level = "C2"
        elif dif_res < 0.3:
            level = "C1"
        elif coverage < 0.5:
            level = "B2"
        elif coverage < 0.7:
            level = "B1"
        elif coverage < 0.9:
            level = "A2"
        else:
            level = "A1"

        recommended = sorted(list(unknown)[:5])

        return {
            "total_words": total,
            "known_words": known_count,
            "unknown_words": unknown_count,
            "coverage_percent": round(coverage, 2),
            "recommended_words_list": recommended,
            "level": level
        }