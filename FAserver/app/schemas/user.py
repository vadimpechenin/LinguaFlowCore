from datetime import datetime
from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    name: str
    username: str
    email: str
    password: str
    initiallevel: str


class UserRead(BaseModel):
    id: str
    name: str
    username: str
    email: str
    initiallevel: str
    createdat: datetime

    model_config = ConfigDict(from_attributes=True)