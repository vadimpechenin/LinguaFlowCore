import numpy as np

from app.services.models.bert_encod import BertEncoder
from app.services.models.cefr_classifier import CEFRClassifier
from app.services.models.difficulty_pred import DifficultyPredictor
from app.services.models.recommender_engine import RecommendationEngine
from app.services.models.recommender_load import RecommendationLoader


class WordAnalyzer:


   def __init__(self):

       self.encoder = BertEncoder()
       self.cefr = CEFRClassifier()
       self.rec = RecommendationLoader()
       self.rec_eng = RecommendationEngine()
       self.dif_pred = DifficultyPredictor()
       self.embedding = None

   def calc_embedding(self, words):
        self.embedding = self.encoder.encode(words)

   def analyze(self, words):
       words_ = self.text_extraction(words)
       self.calc_embedding(words_)
       cefr = self.cefr.predict(self.embedding)
       results = []

       for idx in range(len(words)):
           results.append({
               "id": words[idx].id,
               "word": words_[idx],
               "cefr": cefr[idx],
               "embedding": self.embedding[idx].tolist()
           })

       return results

   def dif_predictor(self, words):
       self.calc_embedding(words)
       dif_res = self.dif_pred.predict(self.embedding)
       return sum(dif_res)/len(dif_res)

   def recommend(self, words):
       analize_results = self.analyze(words)
       #words_ = self.text_extraction(words)
       #embedding = self.encoder.encode(words_)
       scores = []
       for item in analize_results:
           scores.append(self.rec_eng.recommend(np.asarray(item["embedding"]),self.rec.embeddings)[0])

       results = []

       for idx in range(len(words)):
           if (scores[idx]<0.7):
               results.append({
                   "id": analize_results[idx]["id"],
                   "texten": analize_results[idx]["word"],
                   "difficultylevel": analize_results[idx]["cefr"]
               })

       return results
   def text_extraction(self, words):
       results = []
       for word in words:
           results.append(word.texten)

       return results