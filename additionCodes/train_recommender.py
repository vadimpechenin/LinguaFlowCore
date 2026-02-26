"""
создаёт embeddings слов
"""

import joblib

pl_tokenizer = 1


if (pl_tokenizer==0):
    from sentence_transformers import SentenceTransformer
else:
    import torch
    from transformers import AutoTokenizer, AutoModel

from additionCodes.load_df import load_df
from utils.commonUtils import CommonUtils

#Путь к папке
path = CommonUtils.get_project_root()

MODEL_PATH = path + "\\weights_for_ML\\recommender.pkl"

print("Loading dataset")


df, X_column_name,y_column_name = load_df(path)


print("Loading encoder")


if (pl_tokenizer==0):
    encoder = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Encoding words...")

    df["embedding"] = list(

        encoder.encode(
            df[X_column_name].tolist(),
            show_progress_bar=True
        )
    )
else:
    encoder_tokenizer = AutoTokenizer.from_pretrained(
        "sentence-transformers/all-MiniLM-L6-v2"
    )
    encoder = AutoModel.from_pretrained(
        "sentence-transformers/all-MiniLM-L6-v2"
    )
    encoder.eval()

    inputs = encoder_tokenizer(
        df[X_column_name].tolist(),
        return_tensors="pt",
        padding=True,
        truncation=True
    )
    with torch.no_grad():
        outputs = encoder(**inputs)
    df["embedding"] = outputs.last_hidden_state.mean(dim=1).squeeze().numpy().tolist()

print("Saving recommender model")


joblib.dump(
    {
        "data": df["embedding"],
        "encoder_name": "all-MiniLM-L6-v2"
    },

    MODEL_PATH

)


print("Done")
