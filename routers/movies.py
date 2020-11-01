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
    """Creates new movie. Only accessible to Admin.

    - **HEADERS**:
        ```
        {
            "Authorization": "Bearer <sample token>"
        }
        ```
    - **REQUEST**:
        ```
        {
            "name": "The Two Towers",
            "director": "Peter Jackson",
            "popularity": 96.0,
            "imdb_score": 9.6,
            "genre": [
                "Adventure"
            ]
        }
        ```
    - **RESPONSE**:
        ```
        {
            "name": "The Two Towers",
            "director": "Peter Jackson",
            "popularity": 96.0,
            "imdb_score": 9.6,
            "movie_id": 249,
            "genre": [
                {
                    "genre": "Adventure"
                }
            ]
        }
        ```
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
    """List/Search/Filter/Sort all movies. 

    **Eg:**
    1. Search by name: ```/movies?name=star```
    2. Search by director: ```/movies?director=peter```
    3. Get movies with imdb_score less than 8.0: ```/movies?imdb_score=lt:8.0```
    4. Get movies with popularity between 60 to 80: ```/movies?popularity=gte:60&popularity=lte:80```
    5. Sort by director: ```/movies?sort=director```
    6. Sort by name(descending): ```/movies?sort=-name```
    7. Get movie with highest imdb_score: ```/movies?sort=-imdb_score&limit=1```
    8. Get movie with 2nd highest popularity: ```/movies?sort=-popularity&skip=1&limit=1```
    9. And other similar operations...<br>

    **Note**: Search/Filter/Sort currently not supported on `genre`.

    - **REQUEST**:
        ```
        {}
        ```
    - **RESPONSE**:
        ```
        [
            {
                "name": "The Godfather",
                "director": "Francis Ford Coppola",
                "popularity": 92.0,
                "imdb_score": 9.2,
                "movie_id": 11,
                "genre": [
                    {
                        "genre": "Crime"
                    },
                    {
                        "genre": "Drama"
                    }
                ]
            },
            ....
            {
                "name": "Il buono, il brutto, il cattivo.",
                "director": "Sergio Leone",
                "popularity": 90.0,
                "imdb_score": 9.0,
                "movie_id": 43,
                "genre": [
                    {
                        "genre": "Adventure"
                    },
                    {
                        "genre": "Western"
                    }
                ]
            },
        ]
        ```
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
    """Read a movie.

    - **REQUEST**:
        ```
        {}
        ```
    - **RESPONSE**:
        ```
        {
            "name": "The Two Towers",
            "director": "Peter Jackson",
            "popularity": 96.0,
            "imdb_score": 9.6,
            "movie_id": 249,
            "genre": [
                {
                    "genre": "Adventure"
                }
            ]
        }
        ```
    """ 
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
    """Update a movie. Only accessible to Admin.

    - **HEADERS**:
        ```
        {
            "Authorization": "Bearer <sample token>"
        }
        ```
    - **REQUEST**:
        ```
        {
            "name": "The Two Towers",
            "director": "Peter Jackson",
            "popularity": 96.0,
            "imdb_score": 9.6,
            "genre": [
                "Adventure",
                "Fiction"
            ]
        }
        ```
    - **RESPONSE**:
        ```
        {
            "name": "The Two Towers",
            "director": "Peter Jackson",
            "popularity": 96.0,
            "imdb_score": 9.6,
            "movie_id": 249,
            "genre": [
                {
                    "genre": "Adventure"
                },
                {
                    "genre: "Fiction"
                }
            ]
        }
        ```
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
    """Delete a movie. Only accessible to Admin.

    - **HEADERS**:
        ```
        {
            "Authorization": "Bearer <sample token>"
        }
        ```
    - **REQUEST**:
        ```
        {}
        ```
    - **RESPONSE**:
        ```
        {
            "detail": "Resource deleted"
        }
        ```
    """
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=constants.OPERATION_NOT_PERMITTED)
    MovieHandler.delete_movie(db, movie_id=movie_id)
    return {constants.DETAIL: constants.RESOURCE_DELETED}
