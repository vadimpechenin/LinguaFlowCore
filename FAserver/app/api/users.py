from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.user import UserResponse
from app.api.deps import get_current_user, get_current_user2
from app.db.models.user import User
from jose import jwt, JWTError
from app.crud.security import SECRET_KEY, ALGORITHM

from app.crud.user import get_user
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(prefix="/users", tags=["users"])



#TODO не понятно, работает ли
@router.get("/me", response_model=UserResponse)
def get_me(user= Depends(get_current_user2)):
    return user

@router.get("/me2")
def get_me2(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        userid: str = payload.get("sub")
    except JWTError:
        raise HTTPException(401, "Invalid token")

    user = db.query(User).get(userid)
    if not user:
        raise HTTPException(404, "User not found")
    return user


@router.get("/{username}", response_model=UserResponse)
def read_user(username: str, db: Session = Depends(get_db)):
    user = get_user(db, username)
    if not user:
        raise HTTPException(404, "User not found")
    return user


