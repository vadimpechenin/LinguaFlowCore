#TODO не реализована, еще делать и тестировать
from pathlib import Path

from app.core.common_utils import CommonUtils

import os
from dotenv import load_dotenv


load_dotenv()

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEIGHTS_DIR = os.getenv("WEIGHTS_DIR", os.path.join(BASE_DIR, "..", "weights"))
#WEIGHTS_DIR = os.getenv("WEIGHTS_DIR", "/weights")

ML_SERVICE_URL = "http://localhost:8001/ml"

#Пути к весам сетей
SENTENCE_NAME = "sentence_transformers_cache"
CERF_NAME = "cerf_predictor.pkl"
REC_NAME = "recommender.pkl"
DIF_NAME = "difficulty_predictor.pkl"

#Путь к загружаемым данным
filename = "Books_Vocabulary_B1-C1.xlsx"
path = CommonUtils.get_global_project_root()
EXCEL_WORDS_PATH = Path(path + "\\documents\\" + filename)
#EXCEL_WORDS_PATH = Path("D:\\" + filename)
SHEET_NAME = "The_Secret_Garden"
#SHEET_NAME = "Treasure_Island"
REQUIRED_COLUMNS = {
    "Word / Expression",
    "Transcription (BrE)",
    "Translation (RU)",
    "Part of Speech",
    "Level",
    "Example from the book",
}