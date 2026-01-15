"""
Класс для хранения значений таблицы текстов
"""
from pathlib import Path
import os


class TextsParameters():
    def __init__(self, fileName):
        cwd = os.getcwd()
        cwd_ = cwd.split("\\")
        path = "D:"
        for c in cwd_[1:-2]:
            path = path + "\\" + c
        path = path + "\\documents\\" + fileName
        self.TEXTS_FILE_PATH = Path(path)
        self.userid = 'b83618b2915447688156f1106b7be703'