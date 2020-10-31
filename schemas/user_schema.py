from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    is_admin: bool

    class Config:
        orm_mode = True
