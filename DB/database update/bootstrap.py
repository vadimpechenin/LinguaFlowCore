from config import config
from config.allParameters import AllParameters
from core.session import SQLDataBase
from core.support.UUIDClass import UUIDClass

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

        res = config.SQLDataBaseObj.select_all_params_in_table(config.AllParametersObj.namesOfTables.UsersName)
        g = 0
        """
        # Создание таблицы Users
        parameter =UserParameter(config.SQLDataBaseObj,
                                    config.AllParametersObj.namesOfTables.UsersName,
                                    config.AllParametersObj.usersParameters,
                                    config.UUIDClassObj)

        config.MainHandlerObj.initFunction(0, parameter)
        """
