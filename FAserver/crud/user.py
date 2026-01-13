from sqlalchemy.orm import Session

from db.core.support.UUIDClass import UUIDClass
from db.models import User, UserSettings
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, name: str, username: str, email: str, password: str, initiallevel: str) -> User:

    hashed = pwd_context.hash(password)
    ID = UUIDClass.geterateUUIDWithout_()
    user = User(id=ID, name=email, username=email, email=email, password=hashed, initiallevel=initiallevel)
    db.add(user)
    db.flush()

    settings = UserSettings(userid=user.id,
                            interfacelanguage = 'ru',
                            learninglanguage= 'en',
                            preferredvoice = 'en',
                            dailywordlimit=20)

    db.add(settings)

    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()