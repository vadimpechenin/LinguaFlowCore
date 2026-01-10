from handlers.baseCommandHandlerParameter import BaseCommandHandlerParameter

class UserSettingsParameter(BaseCommandHandlerParameter):
    def __init__(self, nameOfDatabase, nameOfTable):
        self.nameOfDatabase = nameOfDatabase
        self.nameOfTable = nameOfTable