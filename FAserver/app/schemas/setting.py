from datetime import datetime
from pydantic import BaseModel, ConfigDict


class SettingResponse(BaseModel):
    userid: str
    createdat: str= "ru"
    learninglanguage: str= "en"
    preferredvoice: str
    dailywordlimit: int
    enableaudio: bool
    enablenotifications: bool
    timezone: str

    model_config = ConfigDict(from_attributes=True)

class SettingUpdate(BaseModel):
    createdat: str | None
    learninglanguage: str | None
    preferredvoice: str | None
    dailywordlimit: int | None
    enableaudio: bool | None
    enablenotifications: bool | None
    timezone: str | None

    model_config = ConfigDict(from_attributes=True)