"""
Класс для классификации уровня сложности слов
"""
import joblib
import os

from app.core.common_utils import CommonUtils
from app.core.settings import CERF_NAME, WEIGHTS_DIR


class CEFRClassifier:


   def __init__(self):
       """
              cwd = os.getcwd()
              cwd_ = cwd.split("\\")
              path = cwd_[0]
              for c in cwd_[1:-3]:
                  path = path + "\\" + c
              """
       #path = CommonUtils.get_global_project_root()
       #texts_file_path = path + "\\weights_for_ML\\" + CERF_NAME
       texts_file_path = os.path.join(WEIGHTS_DIR, CERF_NAME)
       if not os.path.exists(texts_file_path):
           raise FileNotFoundError(f"Weights not found: {texts_file_path}")
       else:
           print(f"Loading weights from: {texts_file_path}")
       data = joblib.load(texts_file_path)
       self.model = data["model"]


   def predict(self, embedding):

       return self.model.predict(
           embedding
       )
