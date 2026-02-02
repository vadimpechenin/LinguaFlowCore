from datetime import datetime, timedelta
from jose import jwt
import hashlib


SECRET_KEY = "SUPER_SECRET_KEY"
ALGORITHM = "MD5"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def hash_password(password: str) -> str:
    h = hashlib.md5(password.encode('utf-8'))
    return h.hexdigest()

def verify_password(stored_password, provided_password):
    #Почему-то не работает на одном и том же пароле
    password_hash = hashlib.md5((provided_password).encode('utf-8')).hexdigest()
    return password_hash == stored_password


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
