from sqlalchemy.orm import Session

from app.db.core.support.UUIDClass import UUIDClass
from app.db.models import User, UserSettings


def replace_fields(obj1, obj2):
    # Получаем все поля из obj2
    fields = obj2.__dict__.keys()

    # Создаем словарь для хранения замен
    replacements = {k: getattr(obj2, k) for k in fields}

    # Проходим по всем полям obj1
    for field in obj1.__dict__.keys():
        # Если поле есть в replacements, заменяем
        if field in replacements:
            if getattr(obj2, field) is not None:
                setattr(obj1, field, replacements[field])

def update_settings_(db: Session, update_Data, settings) -> bool:
    try:
        replace_fields(settings, update_Data)
        db.commit()
        db.refresh(settings)
    except:
        return False
    return True


def get_settings(db: Session, userid: str) -> UserSettings | None:
    return db.query(UserSettings).filter(UserSettings.userid == userid).first()