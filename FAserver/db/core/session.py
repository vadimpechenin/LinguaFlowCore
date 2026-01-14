"""
Класс для работы с базой данных
engine — singleton

SessionLocal — фабрика

1 HTTP request = 1 DB session

commit / rollback — в dependency

CRUD работает с Session, а не с БД-классом
"""
from sqlalchemy import create_engine
from typing import Generator
from sqlalchemy.orm.session import sessionmaker, Session

from db.core.support.supportFunctions import resultproxy_to_dict

from db.config.config import DATABASE_URI

from contextlib import contextmanager
from db.core.base import Base



class SQLDataBase():
    """
    SQLAlchemy оболочка для FastAPI (sync)
    """

    def __init__(self,
        database_uri: str = DATABASE_URI,
        echo: bool = False,
        ):
        self.engine = create_engine(database_uri,
                                    pool_pre_ping = True,
                                    pool_size=10,
                                    max_overflow=20,
                                    echo=echo,
                                    future=True,
                                )

        self.SessionLocal = sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
            class_=Session,
        )

    def create_all(self) -> None:
        #Метод для создания таблиц и базы данных
       Base.metadata.create_all(self.engine)

    def drop_all(self) -> None:
        Base.metadata.drop_all(bind=self.engine)

    def recreate_all(self) -> None:
        self.drop_all()
        self.create_all()

    def get_session(self) -> Session:
        """
        Создание SQLAlchemy сессии
        """
        return self.SessionLocal()

    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        """
        Сессия с контекстным управлением (полезно для скриптов и командной строки)
        """
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    """
    def databaseAddCommit(self,type_object):
        self.session.add(type_object)
        self.session.commit()

    def databaseAddListCommit(self,object_list):
        self.session.bulk_save_objects(object_list)
        self.session.commit()

    @contextmanager
    def session_scope(self):
        session = self.session
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def sessionCloseAll(self):
        session = self.session
        session.close_all()

    def select_all_params_in_table(self, name):
        # Функция для подачи запроса
        request_str = "SELECT * \
                              FROM \
                              " + str(name)
        #s = self.session.query(ParameterDescriptions)
        s = self.session.execute(request_str)
        result_of_query = resultproxy_to_dict(s)
        #result_of_query = result_query_to_dict(s)
        return result_of_query
    """