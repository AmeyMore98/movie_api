from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError

from schemas import (
    movie_schema,
    user_schema,
    token_schema
)
from database import SessionLocal, engine, Base
from services import (
    auth_service, 
    jwt_service,
    MovieHandler,
    UserHandler
)

Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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
        detail="Could not validate credentials",
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
@app.post("/movies/", status_code=201, response_model=movie_schema.Movie)
def create_movie(
    movie: movie_schema.MovieCreate, 
    db: Session = Depends(get_db),
    user: user_schema.User = Depends(get_current_user)
):
    """Creates a new Movie.
    """
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Operation not permitted")
    return MovieHandler.create_movie(db, movie=movie)

@app.get("/movies/", response_model=List[movie_schema.Movie])
def get_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all available movies.
    """
    movies = MovieHandler.get_movies(db, skip=skip, limit=limit)
    return movies

@app.get("/movies/{movie_id}", response_model=movie_schema.Movie)
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = MovieHandler.get_movie(db, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Resource not found")
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
        raise HTTPException(status_code=403, detail="Operation not permitted")
    return MovieHandler.update_movie(db, movie=movie, movie_id=movie_id)

@app.delete("/movies/{movie_id}", status_code=204)
def delete_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    user: user_schema.User = Depends(get_current_user)
):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Operation not permitted")
    return MovieHandler.delete_movie(db, movie_id=movie_id)


# Authentication endpoints
@app.post("/token", response_model=token_schema.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={"WWW-Authenticate": "Bearer"}            
        )
    access_token = jwt_service.create_access_token(
        data={'sub': user.username}
    )

    return {"access_token": access_token, "token_type": "bearer"}

