from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.user import UserResponse
from app.api.deps import get_current_user
from app.db.models.user import User

from app.crud.user import get_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{username}", response_model=UserResponse)
def read_user(username: str, db: Session = Depends(get_db)):
    user = get_user(db, username)
    if not user:
        raise HTTPException(404, "User not found")
    return user

#TODO не понятно, работает ли
@router.get("/me", response_model=UserResponse)
def get_me(user= Depends(get_current_user)):
    return user
