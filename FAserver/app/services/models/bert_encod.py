import os

import joblib
import torch
from transformers import AutoTokenizer, AutoModel

from app.core.common_utils import CommonUtils
#from sentence_transformers import SentenceTransformer

from app.core.settings import CERF_NAME


class BertEncoder:

   def __init__(self):
       """
       cwd = os.getcwd()
       cwd_ = cwd.split("\\")
       path = cwd_[0]
       for c in cwd_[1:-3]:
           path = path + "\\" + c
       """
       path = CommonUtils.get_global_project_root()
       texts_file_path = path + "\\weights_for_ML\\" + CERF_NAME
       print(texts_file_path)
       data = joblib.load(texts_file_path)
       encoder_name = data["encoder_name"]
       self.tokenizer = AutoTokenizer.from_pretrained(
           "sentence-transformers/" + encoder_name
       )
       self.model = AutoModel.from_pretrained(
           "sentence-transformers/" + encoder_name
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
