from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    name: str
    username: str
    email: str
    password: str
    initiallevel: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
