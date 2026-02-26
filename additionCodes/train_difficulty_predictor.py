"""
Вероятность знания слова
"""


pl_tokenizer = 1


if (pl_tokenizer==0):
    from sentence_transformers import SentenceTransformer
else:
    import torch
    from transformers import AutoTokenizer, AutoModel
import numpy as np
import joblib

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

from additionCodes.load_df import load_df
from utils.commonUtils import CommonUtils

#Путь к папке
path = CommonUtils.get_project_root()

MODEL_PATH = path + "\\weights_for_ML\\difficulty_predictor.pkl"

print("Loading dataset...")
df, X_column_name,y_column_name  = load_df(path)


level_map = {

    "A1": 0.95,
    "A2": 0.8,
    "B1": 0.6,
    "B2": 0.4,
    "C1": 0.2,
    "C2": 0.1
}


df["difficulty"] = df[y_column_name].map(level_map)


print("Loading encoder")


if (pl_tokenizer==0):
    encoder = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Encoding words...")

    X = encoder.encode(
        df[X_column_name].tolist(),
        show_progress_bar=True
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
    X = outputs.last_hidden_state.mean(dim=1)

y = df["difficulty"]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2
)


print("Training")


model = Pipeline([
    ("scaler", StandardScaler()),
    ("reg", HistGradientBoostingRegressor(
        max_iter=500,
        max_depth=8
    ))

])


model.fit(
    X_train,
    y_train
)


pred = model.predict(X_test)


print(
    "RMSE",
    np.sqrt(
        mean_squared_error(
            y_test,
            pred
        )
    )
)


print("Saving")


joblib.dump(

    {
        "model": model,
        "encoder_name": "all-MiniLM-L6-v2"

    },
    MODEL_PATH

)


print("Done")
