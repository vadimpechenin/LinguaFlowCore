from config import config
from config.allParameters import AllParameters
from core.session import SQLDataBase
from core.support.UUIDClass import UUIDClass
from handlers.generateWords.paramsWords import WordsParameter
from handlers.generateSettings.paramsSettings import UserSettingsParameter
from handlers.generateText.paramsTexts import TextsParameter
from handlers.mainHandler import MainHandler


class Bootstrap():

    @staticmethod
    def initEnviroment():
        config.AllParametersObj = AllParameters()
        # Создание объекта подключения к БД
        config.SQLDataBaseObj = SQLDataBase()
        #config.SQLDataBaseObj.db_create()
        config.MainHandlerObj = MainHandler()
        config.UUIDClassObj = UUIDClass()

    @staticmethod
    def run():
        # Создание БД
        # config.SQLDataBaseObj.db_create()
        # Работа с сессией
        config.SQLDataBaseObj.create_session()
        # Уничтожение всего что было в БД (не обязательно)
        #config.SQLDataBaseObj.recreate_database()

        #res = config.SQLDataBaseObj.select_all_params_in_table(config.AllParametersObj.namesOfTables.UsersName)
        if (1==1):
            #Создание таблицы Words
            parameter =WordsParameter(config.SQLDataBaseObj,
                                        config.AllParametersObj.namesOfTables.WordsName,
                                        config.AllParametersObj.wordsParameters,
                                        config.UUIDClassObj)

            config.MainHandlerObj.initFunction(0, parameter)
        if (1 == 1):
            # Создание таблицы UserSettings
            parameter = UserSettingsParameter(config.SQLDataBaseObj,
                                       config.AllParametersObj.namesOfTables.UserSettings)

            config.MainHandlerObj.initFunction(1, parameter)

        if (1 == 1):
            # Создание таблицы Texts
            parameter = TextsParameter(config.SQLDataBaseObj,
                                              config.AllParametersObj.namesOfTables.TextsName,
                                              config.AllParametersObj.textsParameters,
                                              config.UUIDClassObj
                                              )

            config.MainHandlerObj.initFunction(2, parameter)
        g = 0
