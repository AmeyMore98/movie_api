from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, status, Query
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError

from schemas import (
    movie_schema,
    user_schema,
    token_schema
)
from db.database import SessionLocal, engine, Base
from services import (
    auth_service, 
    jwt_service
)
from handlers import (
    MovieHandler,
    UserHandler
)
import constants

Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=constants.CREDENTIALS_NOT_VALID,
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt_service.decode_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = token_schema.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = UserHandler.get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user        

# Movie endpoints
@app.post("/movies/", status_code=status.HTTP_201_CREATED, response_model=movie_schema.Movie)
def create_movie(
    movie: movie_schema.MovieCreate, 
    db: Session = Depends(get_db),
    user: user_schema.User = Depends(get_current_user)
):
    """Creates a new Movie.
    """
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=constants.OPERATION_NOT_PERMITTED)
    return MovieHandler.create_movie(db, movie=movie)

@app.get("/movies/", response_model=List[movie_schema.Movie])
def get_movies(
    name: Optional[str] = None,
    director: Optional[str] = None,
    popularity: Optional[str] = Query(None, regex=constants.POPULARITY_QUERY_REGEX),
    imdb_score: Optional[str] = Query(None, regex=constants.IMDB_SCORE_QUERY_REGEX),
    skip: int = 0, 
    limit: int = 100, 
    sort: Optional[str] = Query('', regex=constants.SORT_REGEX),
    db: Session = Depends(get_db)
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
        filter_args['popularity__'+opearator] = float(val)
    if imdb_score:
        opearator, val = imdb_score.split(':')
        filter_args['imdb_score__'+opearator] = float(val)

    sort_args = sort.split(',') if sort else []

    movies = MovieHandler.get_movies(db, filter_args, sort_args, skip=skip, limit=limit)
    return movies

@app.get("/movies/{movie_id}", response_model=movie_schema.Movie)
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = MovieHandler.get_movie(db, movie_id)
    if movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=constants.RESOURCE_NOT_FOUND)
    return movie

@app.put("/movies/{movie_id}", response_model=movie_schema.Movie)
def update_movie(
    movie_id: int, 
    movie: movie_schema.MovieUpdate,
    db: Session = Depends(get_db),
    user: user_schema.User = Depends(get_current_user)
):
    """Updates an existing Movie.
    """
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=constants.OPERATION_NOT_PERMITTED)
    return MovieHandler.update_movie(db, movie=movie, movie_id=movie_id)

@app.delete("/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    user: user_schema.User = Depends(get_current_user)
):
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=constants.OPERATION_NOT_PERMITTED)
    return MovieHandler.delete_movie(db, movie_id=movie_id)


# User endpoints
@app.post("/users/", status_code=status.HTTP_201_CREATED, response_model=user_schema.User)
def create_user(
    new_user: user_schema.UserCreate, 
    db: Session = Depends(get_db),
    user: user_schema.User = Depends(get_current_user)
):
    """Creates a new User.
    """
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=constants.OPERATION_NOT_PERMITTED
        )
    # new_user.password = auth_service.get_password_hash(new_user.password)
    user_in_db = user_schema.UserInDb(
        **new_user.dict(), 
        hashed_password=auth_service.get_password_hash(new_user.password)
    )
    return UserHandler.create_user(db, user=user_in_db)

@app.get("/users/", response_model=List[user_schema.User])
def get_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """List all available users. 
    """
    users = UserHandler.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{username}", response_model=user_schema.User)
def read_user(username: str, db: Session = Depends(get_db)):
    user = UserHandler.get_user(db, username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=constants.RESOURCE_NOT_FOUND)
    return user

@app.put("/users/{username}", response_model=user_schema.User)
def update_user(
    username: str, 
    new_user: user_schema.UserUpdate,
    db: Session = Depends(get_db),
    user: user_schema.User = Depends(get_current_user)
):
    """Updates an existing User.
    """
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=constants.OPERATION_NOT_PERMITTED)
    # new_user.password = auth_service.get_password_hash(new_user.password)
    user_in_db = user_schema.UserInDb(
        **new_user.dict(), 
        hashed_password=auth_service.get_password_hash(new_user.password)
    )
    return UserHandler.update_user(db, user=user_in_db, username=username)

@app.delete("/users/{username}", status_code=status.HTTP_200_OK)
def delete_user(
    username: str,
    db: Session = Depends(get_db),
    user: user_schema.User = Depends(get_current_user)
):
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=constants.OPERATION_NOT_PERMITTED)
    UserHandler.delete_user(db, username=username)
    return {constants.MESSAGE: constants.RESOURCE_DELETED}


# Authentication endpoints
@app.post("/login", response_model=token_schema.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=constants.INCORRECT_CREDENTIALS,
            headers={"WWW-Authenticate": "Bearer"}            
        )
    access_token = jwt_service.create_access_token(
        data={'sub': user.username}
    )

    return {"access_token": access_token, "token_type": "bearer"}
