"""
Класс для классификации степени сложности слов
"""
import joblib
import os

from app.core.settings import DIF_NAME


class DifficultyPredictor:


   def __init__(self):
       cwd = os.getcwd()
       cwd_ = cwd.split("\\")
       path = cwd_[0]
       for c in cwd_[1:-3]:
           path = path + "\\" + c
       texts_file_path = path + "\\weights_for_ML\\" + DIF_NAME
       data = joblib.load(texts_file_path)
       self.model = data["model"]


   def predict(self, embedding):

       return self.model.predict(
           embedding
       )