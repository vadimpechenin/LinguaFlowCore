#Приложение, генерирующее базу данных для проекта

#Импорт стартового класса
from bootstrap import Bootstrap

if __name__ == '__main__':

    Bootstrap.initEnviroment()
    Bootstrap.run()