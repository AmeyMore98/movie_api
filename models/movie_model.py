from sqlalchemy import (
    Column,
    Integer, 
    String, 
    Float, 
    Table,
    ForeignKey
)
from sqlalchemy.orm import relationship, Session

from database import Base

movie_genre_association = Table(
    'movie_genre',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey("movies.movie_id")),
    Column('genre', String, ForeignKey("genres.genre"))
)

class Movie(Base):
    __tablename__ = 'movies'

    movie_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    director = Column(String, nullable=False)
    popularity = Column(Float, nullable=False)
    imdb_score = Column(Float, nullable=False)
    genre = relationship(
        "Genre",
        secondary=movie_genre_association
    )

class Genre(Base):
    __tablename__ = 'genres'

    genre = Column(String, primary_key=True)

