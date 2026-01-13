from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.deps import get_db
from schemas.user import UserCreate, UserRead
from crud.user import create_user, get_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead)
def register(data: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, data.email, data.password)


@router.get("/{username}", response_model=UserRead)
def read_user(username: str, db: Session = Depends(get_db)):
    user = get_user(db, username)
    if not user:
        raise HTTPException(404, "User not found")
    return user