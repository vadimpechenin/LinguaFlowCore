#TODO не реализована, еще делать и тестировать
from pathlib import Path

from app.core.common_utils import CommonUtils

ML_SERVICE_URL = "http://localhost:8001/ml"

#Пути к весам сетей
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