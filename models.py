from sqlalchemy import (
    Column,
    Integer, 
    String, 
    ForeignKey, 
    Float, 
    Table,
    Boolean
)
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'

    username = Column(String, primary_key=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False)

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

    # genre_id = Column(Integer, primary_key=True, index=True)
    genre = Column(String, primary_key=True)

    def __repr__(self):
        return self.genre
