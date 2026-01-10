from core.support.UUIDClass import UUIDClass
from handlers.baseCommandHandler import BaseCommandHandler
from models.word import Word
import pandas as pd

class GenerateWordsCommandHandler(BaseCommandHandler):
    def __init__(self):
        pass

    def execute(self, parameters):
        # Запрос к базе данных на заполнение данных
        data_base = parameters.nameOfDatabase
        data_base.create_session()

        df = pd.read_excel(parameters.excel_words_part)

        if not parameters.required_columns.issubset(df.columns):
            raise ValueError("Excel file has missing required columns")

        words = []
        for _, row in df.iterrows():
            ID = UUIDClass.geterateUUIDWithout_()
            parameters.uuidObject.wordsIDList.append(ID)
            word = Word(
                id = ID,
                texten=row["Word / Expression"],
                transcription=row.get("Transcription (BrE)"),
                textl=row.get("Translation (RU)"),
                partofspeech=row.get("Part of Speech"),
                examplesentence=row.get("Example from the book"),
                difficultylevel=row["Level"],
                audiourl=None,  # отсутствует в Excel
            )
            words.append(word)
        data_base.databaseAddListCommit(words)
        print(f"✅ Inserted {len(words)} words")
        return True