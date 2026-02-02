from datetime import datetime
from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    id: str
    name: str
    username: str
    email: str
    initiallevel: str
    createdat: datetime

    model_config = ConfigDict(from_attributes=True)