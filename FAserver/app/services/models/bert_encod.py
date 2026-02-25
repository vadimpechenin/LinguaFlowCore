import torch
from transformers import AutoTokenizer, AutoModel


class BertEncoder:

   def __init__(self):

       self.tokenizer = AutoTokenizer.from_pretrained(
           "sentence-transformers/all-MiniLM-L6-v2"
       )
       self.model = AutoModel.from_pretrained(
           "sentence-transformers/all-MiniLM-L6-v2"
       )
       self.model.eval()

   def encode(self, word):

       inputs = self.tokenizer(
           word,
           return_tensors="pt"
       )
       with torch.no_grad():
           outputs = self.model(**inputs)
       embedding = outputs.last_hidden_state.mean(dim=1)

       return embedding.squeeze().numpy()
