from typing import List, Optional

from fastapi import APIRouter
from fastapi import Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from schemas import (
    movie_schema,
    user_schema,
)
from handlers import (
    MovieHandler
)
from routers import dependancies
from constants import constants

router = APIRouter()

# Movie endpoints
@router.post("/movies", status_code=status.HTTP_201_CREATED, response_model=movie_schema.Movie)
def create_movie(
    movie: movie_schema.MovieCreate, 
    db: Session = Depends(dependancies.get_db),
    user: user_schema.User = Depends(dependancies.get_current_user)
):
    """Creates a new Movie.
    """
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=constants.OPERATION_NOT_PERMITTED)
    return MovieHandler.create_movie(db, movie=movie)

@router.get("/movies", response_model=List[movie_schema.Movie])
def get_movies(
    name: Optional[str] = None,
    director: Optional[str] = None,
    popularity: Optional[str] = Query(None, regex=constants.POPULARITY_QUERY_REGEX),
    imdb_score: Optional[str] = Query(None, regex=constants.IMDB_SCORE_QUERY_REGEX),
    skip: int = 0, 
    limit: int = 100, 
    sort: Optional[str] = Query('', regex=constants.SORT_REGEX),
    db: Session = Depends(dependancies.get_db)
):
    """List/Filter/Paginate/Sort all available movies. 
    """
    filter_args = {}
    if name:
        filter_args['name'] = name
    if director:
        filter_args['director'] = director
    if popularity:
        opearator, val = popularity.split(':')
        filter_args['popularity__' + opearator] = float(val)
    if imdb_score:
        opearator, val = imdb_score.split(':')
        filter_args['imdb_score__' + opearator] = float(val)

    sort_args = sort.split(',') if sort else []

    movies = MovieHandler.get_movies(db, filter_args, sort_args, skip=skip, limit=limit)
    return movies

@router.get("/movies/{movie_id}", response_model=movie_schema.Movie)
def read_movie(movie_id: int, db: Session = Depends(dependancies.get_db)):
    movie = MovieHandler.get_movie(db, movie_id)
    if movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=constants.RESOURCE_NOT_FOUND)
    return movie

@router.put("/movies/{movie_id}", response_model=movie_schema.Movie)
def update_movie(
    movie_id: int, 
    movie: movie_schema.MovieUpdate,
    db: Session = Depends(dependancies.get_db),
    user: user_schema.User = Depends(dependancies.get_current_user)
):
    """Updates an existing Movie.
    """
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=constants.OPERATION_NOT_PERMITTED)
    return MovieHandler.update_movie(db, movie=movie, movie_id=movie_id)

@router.delete("/movies/{movie_id}", status_code=status.HTTP_200_OK)
def delete_movie(
    movie_id: int,
    db: Session = Depends(dependancies.get_db),
    user: user_schema.User = Depends(dependancies.get_current_user)
):
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=constants.OPERATION_NOT_PERMITTED)
    MovieHandler.delete_movie(db, movie_id=movie_id)
    return {constants.DETAIL: constants.RESOURCE_DELETED}
