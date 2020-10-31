from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    is_admin: bool

class UserCreate(UserBase):
    password: str

class UserUpdate(UserCreate):
    pass

class User(UserBase):
    
    class Config:
        orm_mode = True
