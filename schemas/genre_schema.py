from pydantic import BaseModel

class Genre(BaseModel):
    genre: str

    class Config:
        orm_mode = True
