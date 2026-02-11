from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.setting import SettingResponse, SettingUpdate
from app.schemas.user import UserResponse
from app.api.deps import get_current_user
from app.db.models.user import User

from app.crud.setting import get_settings, update_settings_

router = APIRouter(prefix="/user-settings", tags=["usersettings"])


@router.get("", response_model=SettingResponse)
def read_settings(user: User=Depends(get_current_user), db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(404, "User not found")
    user_settings= get_settings(db, user.id)
    if not user_settings:
        raise HTTPException(404, "User settings not found")
    return user_settings


@router.put("", response_model=bool)
def update_settings(data: SettingUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(404, "User not found")
    user_settings = get_settings(db, user.id)
    if not user_settings:
        raise HTTPException(404, "User settings not found")
    result = update_settings_(db, data, user_settings)

    return result