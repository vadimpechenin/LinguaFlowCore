import pandas as pd

from app.core.settings import EXCEL_WORDS_PATH, SHEET_NAME, REQUIRED_COLUMNS


def test_create_words_from_table(client, auth_headers):
    # Загружаем слова из таблицы

    df = pd.read_excel(EXCEL_WORDS_PATH,sheet_name=SHEET_NAME)

    if not REQUIRED_COLUMNS.issubset(df.columns):
        raise ValueError("Excel file has missing required columns")

    words = []
    for _, row in df.iterrows():
        word = {"texten":row["Word / Expression"],
            "transcription":row.get("Transcription (BrE)"),
            "textl":row.get("Translation (RU)"),
            "partofspeech":row.get("Part of Speech"),
            "examplesentence":row.get("Example from the book"),
            "difficultylevel":row["Level"]
                }
        words.append(word)

    response = client.post("/words/from_table", json=words, headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)