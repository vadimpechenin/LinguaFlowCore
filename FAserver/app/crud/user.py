from sqlalchemy.orm import Session

from app.db.core.support.UUIDClass import UUIDClass
from app.db.models import User, UserSettings
from passlib.context import CryptContext
import hashlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    h = hashlib.md5(password.encode('utf-8'))
    return h.hexdigest()

def verify_password(stored_password, provided_password):
    password_hash = hashlib.md5((provided_password).encode('utf-8')).hexdigest()
    return password_hash == stored_password

def create_user(db: Session, name: str, username: str, email: str, password: str, initiallevel: str) -> User:

    hashed = hash_password(password)
    ID = UUIDClass.geterateUUIDWithout_()
    user = User(id=ID, name=name, username=username, email=email, password=hashed, initiallevel=initiallevel)
    db.add(user)
    db.flush()
    db.refresh(user)

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