from typing import List

from pydantic import BaseModel

from schemas import genre_schema

class MovieBase(BaseModel):
    name: str
    director: str
    popularity: float
    imdb_score: float

class MovieCreate(MovieBase):
    genre: List[str]

class Movie(MovieBase):
    movie_id: int
    genre: List[genre_schema.Genre]

    class Config:
        orm_mode = True

