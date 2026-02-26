"""
Прогноз сложности слов
"""


pl_tokenizer = 1

import joblib
if (pl_tokenizer==0):
    from sentence_transformers import SentenceTransformer
else:
    import torch
    from transformers import AutoTokenizer, AutoModel

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from additionCodes.load_df import load_df
from utils.commonUtils import CommonUtils

#Путь к папке
path = CommonUtils.get_project_root()

MODEL_PATH = path + "\\weights_for_ML\\cerf_predictor.pkl"

print("Loading dataset...")
df, X_column_name,y_column_name  = load_df(path)


print("Loading BERT encoder...")

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


y = df[y_column_name]
print("Split train test")


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y
)


print("Training classifier")


model = Pipeline([

    ("scaler", StandardScaler()),
    ("clf", HistGradientBoostingClassifier(
        max_iter=500,
        max_depth=8,
        learning_rate=0.05
    ))
])


model.fit(
    X_train,
    y_train
)


print("Evaluating")


pred = model.predict(X_test)


print(
    classification_report(
        y_test,
        pred
    )
)


print("Saving model")


joblib.dump(

    {
        "model": model,
        "encoder_name": "all-MiniLM-L6-v2"
    },
    MODEL_PATH
)


print("Done")
