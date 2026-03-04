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


   def calc_embedding(self, words):
        return self.encoder.encode(words)


   def get_unknown_words(self, base_words, new_words):
       base_embedding = self.calc_embedding(base_words)
       new_embedding = self.calc_embedding(new_words)
       scores = []
       for item in new_embedding:
           scores.append(self.rec_eng.recommend(np.asarray(item), base_embedding)[0])
       result = []
       for index in range(len(scores)):
           if (scores[index]<0.94):
               result.append(new_words[index])
       return result

   def analyze(self, words):
       words_ = self.text_extraction(words)
       embedding = self.calc_embedding(words_)
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

   def dif_predictor(self, words):
       embedding = self.calc_embedding(words)
       dif_res = self.dif_pred.predict(embedding)
       return sum(dif_res)/len(dif_res)

   def recommend(self, words, limit):
       analize_results = self.analyze(words)
       #words_ = self.text_extraction(words)
       #embedding = self.encoder.encode(words_)
       scores = []
       for item in analize_results:
           scores.append(self.rec_eng.recommend(np.asarray(item["embedding"]),self.rec.embeddings)[0])

       sorted_indices = [i for (i, _) in sorted(enumerate(scores), key=lambda x: x[1])]
       results = []

       for idx in range(limit):
           results.append({
               "id": words[sorted_indices[len(sorted_indices)-idx-1]].id,
               "texten": words[sorted_indices[len(sorted_indices)-idx-1]].texten,
               "transcription": words[sorted_indices[len(sorted_indices)-idx-1]].transcription,
               "textl": words[sorted_indices[len(sorted_indices)-idx-1]].textl,
               "partofspeech": words[sorted_indices[len(sorted_indices)-idx-1]].partofspeech,
               "examplesentence": words[sorted_indices[len(sorted_indices)-idx-1]].examplesentence,
               "difficultylevel": words[sorted_indices[len(sorted_indices)-idx-1]].difficultylevel,
               "audiourl": words[sorted_indices[len(sorted_indices)-idx-1]].audiourl,
               "createdat": words[sorted_indices[len(sorted_indices)-idx-1]].createdat,
           })

       return results


   def text_extraction(self, words):
       results = []
       for word in words:
           results.append(word.texten)

       return results