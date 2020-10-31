from sqlalchemy.orm import Session
from fastapi import HTTPException

from models import movie_model
from schemas import movie_schema
from services import utils

class MovieHandler:

    @staticmethod
    def get_movie(db: Session, movie_id: int):
        return db.query(movie_model.Movie).get(movie_id)

    @staticmethod
    def create_movie(db: Session, movie: movie_schema.MovieCreate):
        movie = movie.dict()
        db_movie = movie_model.Movie(**movie)
        db_movie.genre = list(map(lambda x: utils.get_or_create(db, movie_model.Genre, genre=x.strip()), movie['genre']))
        db.add(db_movie)
        db.commit()
        db.refresh(db_movie)
        return db_movie

    @staticmethod
    def update_movie(db: Session, movie: movie_schema.MovieUpdate, movie_id: int):
        existing_movie = db.query(movie_model.Movie).get(movie_id)
        if not existing_movie:
            raise HTTPException(status_code=404, detail="Resource not found")

        for key, value in movie.dict().items():
            if key == 'genre':
                setattr(
                    existing_movie,
                    key, 
                    list(
                        map(
                            lambda x: utils.get_or_create(db, movie_model.Genre, genre=x.strip()), 
                            value
                        )
                    )
                )
            else:
                setattr(existing_movie, key, value)

        db.add(existing_movie)
        db.commit()
        db.refresh(existing_movie)
        return existing_movie

    @staticmethod
    def get_movies(db: Session, filter_args: dict = {}, sort_args: list = [], skip: int = 0, limit: int = 100):
        filters = utils.get_filter_by_args(movie_model.Movie, filter_args)
        sorters = utils.get_sorter_by_args(movie_model.Movie, sort_args)
        return db.query(movie_model.Movie).filter(*filters).order_by(*sorters).offset(skip).limit(limit).all()

    @staticmethod
    def delete_movie(db: Session, movie_id: int):
        movie = db.query(movie_model.Movie).get(movie_id)
        if movie:
            db.delete(movie)
            db.commit()
            return 
