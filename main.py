from fastapi import FastAPI

from db.database import engine, Base
from routers import (
    users,
    movies,
    auth
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Imdb API",
    description="Movie API similar to Imdb",
    version="0.1.0"
)
app.include_router(users.router)
app.include_router(movies.router)
app.include_router(auth.router)
