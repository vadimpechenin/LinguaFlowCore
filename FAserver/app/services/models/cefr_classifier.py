"""
Класс для классификации уровня сложности слов
"""
import joblib
import os

from app.core.settings import CERF_NAME


class CEFRClassifier:


   def __init__(self):
       cwd = os.getcwd()
       cwd_ = cwd.split("\\")
       path = cwd_[0]
       for c in cwd_[1:-3]:
           path = path + "\\" + c
       texts_file_path = path + "\\weights_for_ML\\" + CERF_NAME
       self.model = joblib.load(
           texts_file_path
       )


   def predict(self, embedding):

       return self.model.predict(
           [embedding]
       )[0]
