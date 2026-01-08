"""
Описывает базовый класс для заполнения всех таблиц
"""


class MainHandler():
    def __init__(self):
        self.dict = {}

    def initFunction(self,code_request, parameter):
        result = None
        if code_request in self.dict:
            handler = self.dict[code_request]
            result = handler.execute(parameter)

        return result