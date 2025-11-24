import re
from utils.commonUtils import CommonUtils

def find_first_sentence(phrase, text):
    # Разбиваем на предложения
    sentences = re.split(r'(?<=[.!?])\s+', text)

    # Подготовка фразы для поиска
    # Например: "contrary scowl" → r"\bcontrary\s+scowl\b"
    phrase_pattern = r'\b' + r'\s+'.join(map(re.escape, phrase.split())) + r'\b'

    pattern = re.compile(phrase_pattern, re.IGNORECASE)

    for sentence in sentences:
        if pattern.search(sentence):
            return sentence.strip()

    return None


def main():
    # ===== Загрузка текста =====
    path = CommonUtils.get_project_root()
    text_file = path + "\\documents\\The secret garden.txt"
    with open(text_file, "r", encoding="utf-8") as f:
        text = f.read()

    # ===== Список слов и выражений =====
    items = [
        "gloves",
        "contrary scowl",
        "frock",
        "brocade",
        "snowdrops",
        "queer feeling",
        "make up one's mind"  # пример фразового выражения
    ]

    # ===== Поиск =====
    for item in items:
        sentence = find_first_sentence(item, text)
        if sentence:
            print(f"{item}: {sentence}")
        else:
            print(f"{item}: ❌ не найдено")


if __name__ == "__main__":
    main()
