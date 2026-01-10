from core.support.UUIDClass import UUIDClass
from handlers.baseCommandHandler import BaseCommandHandler
from models.text import Text
import pandas as pd

class GenerateTextsCommandHandler(BaseCommandHandler):
    def __init__(self):
        pass

    def execute(self, parameters):
        # Запрос к базе данных на заполнение данных
        data_base = parameters.nameOfDatabase
        data_base.create_session()

        content = parameters.texts_file_path.read_text(encoding="utf-8")

        blocks = content.split("=== TEXT ===")

        texts = []

        for block in blocks:
            ID = UUIDClass.geterateUUIDWithout_()
            parameters.uuidObject.textsIDList.append(ID)
            if "=== END ===" not in block:
                continue

            header, body = block.split("\n\n", 1)

            title = None

            for line in header.splitlines():
                if line.startswith("Title:"):
                    title = line.replace("Title:", "").strip()

            text_content = body.replace("=== END ===", "").strip()

            if not title or not text_content:
                continue

            text = Text(
                id = ID,
                userid = parameters.userid,
                title=title,
                content=text_content
            )
            texts.append(text)
        data_base.databaseAddListCommit(texts)
        print(f"✅ Inserted {len(texts)} texts")
        return True