from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError

import crud
import models
from schemas import (
    movie_schema,
    user_schema,
    token_schema
)
from database import SessionLocal, engine
from services import (
    auth_service, 
    jwt_service,
)

models.Base.metadata.create_all(bind=engine)

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
    except JWTError as e:
        print(e)
        raise credentials_exception
    user = crud.get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user        

# Movie endpoints
@app.post("/movies/", response_model=movie_schema.Movie)
def create_movie(
    movie: movie_schema.MovieCreate, 
    db: Session = Depends(get_db),
    user: user_schema.User = Depends(get_current_user)
):
    """Creates a new Movie.
    """
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Operation not permitted")
    return crud.create_movie(db, movie=movie)

@app.get("/movies/", response_model=List[movie_schema.Movie])
def get_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    movies = crud.get_movies(db, skip=skip, limit=limit)
    return movies


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

