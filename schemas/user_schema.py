from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: EmailStr
    is_admin: bool

class UserCreate(UserBase):
    password: str

class UserUpdate(UserCreate):
    pass

class UserInDb(UserBase):
    hashed_password: str

class User(UserBase):
    
    class Config:
        orm_mode = True
