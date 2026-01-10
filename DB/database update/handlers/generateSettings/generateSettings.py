from handlers.baseCommandHandler import BaseCommandHandler
from models import UserSettings


class GenerateUserSettingsCommandHandler(BaseCommandHandler):
    def __init__(self):
        pass

    def execute(self, parameters):
        # Запрос к базе данных на заполнение данных
        data_base = parameters.nameOfDatabase
        data_base.create_session()

        settings = UserSettings(
            userid='b83618b2915447688156f1106b7be703',  # предполагаем, что пользователь уже существует
            interfacelanguage = 'ru',
            learninglanguage= 'en',
            preferredvoice = 'en',
            dailywordlimit=20
        )

        data_base.databaseAddCommit(settings)
        print("✅ User settings created")
        return True