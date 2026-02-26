import numpy as np

from app.services.models.bert_encod import BertEncoder
from app.services.models.cefr_classifier import CEFRClassifier
from app.services.models.recommender_engine import RecommendationEngine
from app.services.models.recommender_load import RecommendationLoader


class WordAnalyzer:


   def __init__(self):

       self.encoder = BertEncoder()
       self.cefr = CEFRClassifier()
       self.rec = RecommendationLoader()
       self.rec_eng = RecommendationEngine()

   def analyze(self, words):
       words_ = self.text_extraction(words)
       embedding = self.encoder.encode(words_)
       cefr = self.cefr.predict(embedding)
       results = []

       for idx in range(len(words)):
           results.append({
               "id": words[idx].id,
               "word": words_[idx],
               "cefr": cefr[idx],
               "embedding": embedding[idx].tolist()
           })

       return results

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