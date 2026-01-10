from handlers.baseCommandHandlerParameter import BaseCommandHandlerParameter

class WordsParameter(BaseCommandHandlerParameter):
    def __init__(self, nameOfDatabase, nameOfTable, parameters,uuidObject):
        self.nameOfDatabase = nameOfDatabase
        self.nameOfTable = nameOfTable
        self.excel_words_part = parameters.EXCEL_WORDS_PATH
        self.required_columns = parameters.required_columns
        self.uuidObject = uuidObject