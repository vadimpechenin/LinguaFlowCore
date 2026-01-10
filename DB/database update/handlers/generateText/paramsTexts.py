from handlers.baseCommandHandlerParameter import BaseCommandHandlerParameter

class TextsParameter(BaseCommandHandlerParameter):
    def __init__(self, nameOfDatabase, nameOfTable, parameters,uuidObject):
        self.nameOfDatabase = nameOfDatabase
        self.nameOfTable = nameOfTable
        self.texts_file_path = parameters.TEXTS_FILE_PATH
        self.userid = parameters.userid
        self.uuidObject = uuidObject