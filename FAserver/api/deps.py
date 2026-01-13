from db.core.session import SQLDataBase


def get_db():
    db = SQLDataBase()
    db.create_session()
    try:
        yield db.session
    finally:
        db.sessionCloseAll()