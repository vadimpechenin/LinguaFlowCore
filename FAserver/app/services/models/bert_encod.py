import os

import joblib
import torch
from transformers import AutoTokenizer, AutoModel

from app.core.common_utils import CommonUtils
#from sentence_transformers import SentenceTransformer

from app.core.settings import CERF_NAME, SENTENCE_NAME, WEIGHTS_DIR

class BertEncoder:

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
       encoder_name = data["encoder_name"]
       #cache_folder = "sentence-transformers/" + encoder_name
       cache_folder = os.path.join(WEIGHTS_DIR, SENTENCE_NAME)
       if not os.path.exists(cache_folder):
           raise FileNotFoundError(f"sentence_transformers_cache not found: {cache_folder}")
       else:
            print(f"Loading sentence_transformers_cache from: {cache_folder}")
       self.tokenizer = AutoTokenizer.from_pretrained(
           cache_folder
       )
       self.model = AutoModel.from_pretrained(
           cache_folder
       )
       self.model.eval()

   def encode(self, words):
       inputs = self.tokenizer(
           words,
           return_tensors="pt",
            padding=True,
            truncation=True
       )
       with torch.no_grad():
           outputs = self.model(**inputs)
       embedding = outputs.last_hidden_state.mean(dim=1)

       return embedding.squeeze().numpy()
