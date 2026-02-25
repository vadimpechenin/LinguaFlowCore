from app.services.models.bert_encod import BertEncoder
from app.services.models.cefr_classifier import CEFRClassifier


class WordAnalyzer:


   def __init__(self):

       self.encoder = BertEncoder()
       self.cefr = CEFRClassifier()


   def analyze(self, words):

       results = []

       for word in words:

           embedding = self.encoder.encode(word)

           cefr = self.cefr.predict(embedding)

           results.append({
               "word": word,
               "cefr": cefr,
               "embedding": embedding.tolist()
           })

       return results
