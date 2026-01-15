"""
Класс для хранения значений таблицы слов
"""
from pathlib import Path
import os


class WordsParameters():
    def __init__(self, fileName):
        cwd = os.getcwd()
        cwd_ = cwd.split("\\")
        path = "D:"
        for c in cwd_[1:-2]:
            path = path + "\\" + c
        path = path + "\\documents\\" + fileName
        self.EXCEL_WORDS_PATH = Path(path)
        self.required_columns = {
                        "Word / Expression",
                        "Transcription (BrE)",
                        "Translation (RU)",
                        "Part of Speech",
                        "Level",
                        "Example from the book",
                    }