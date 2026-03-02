import numpy as np


class RecommendationEngine:


   def recommend(
       self,
       embeddings,
       known_embeddings,
       top_k: int = 6
   ):
       if (len(embeddings.shape)==1):
           scores = [self.cosine_similarity(
               embeddings,
               known_embeddings
           )]
       else:
           scores = []

           for emb in embeddings:
               sim = self.cosine_similarity(
                   emb,
                   known_embeddings
               )
               scores.append(sim)

       return scores


   def cosine_similarity(
       self,
       emb,
       matrix
   ):

       return np.max(
           np.dot(matrix, emb)
           /
           (
               np.linalg.norm(matrix, axis=1)
               *
               np.linalg.norm(emb)
           )
       )
