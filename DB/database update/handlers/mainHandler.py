"""
Описывает базовый класс для заполнения всех таблиц
"""
from handlers.generateSettings.generateSettings import GenerateUserSettingsCommandHandler
from handlers.generateText.generateTexts import GenerateTextsCommandHandler
from handlers.generateWords.generateWords import GenerateWordsCommandHandler


class MainHandler():
    def __init__(self):
        self.dict = {}

        self.dict[0] = GenerateWordsCommandHandler()
        self.dict[1] = GenerateUserSettingsCommandHandler()
        self.dict[2] = GenerateTextsCommandHandler()

    def initFunction(self,code_request, parameter):
        result = None
        if code_request in self.dict:
            handler = self.dict[code_request]
            result = handler.execute(parameter)

        return result