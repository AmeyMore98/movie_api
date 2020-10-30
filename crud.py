from sqlalchemy.orm import Session

import models
from schemas import movie_schema, user_schema

def get_movie(db: Session, movie_id: int):
    return db.query(models.Movie).get(movie_id)

def get_or_create(db: Session, model, **kwargs):
    instance = db.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        db.add(instance)
        db.commit()
        return instance

def create_movie(db: Session, movie: movie_schema.MovieCreate):
    movie = movie.dict()
    db_movie = models.Movie(**movie)
    db_movie.genre = list(map(lambda x: get_or_create(db, models.Genre, genre=x.strip()), movie['genre']))
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

def get_movies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Movie).offset(skip).limit(limit).all()

def get_user(db: Session, username: str):
    return db.query(models.User).filter_by(username=username).first()
