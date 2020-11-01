from fastapi import FastAPI

from db.database import engine, Base
from routers import (
    users,
    movies,
    auth
)

# Create all tables
Base.metadata.create_all(bind=engine)

# Init App
app = FastAPI(
    title="Movie API",
    description="A movie API similar to Imdb",
    version="0.1.0"
)

# Setup routes
app.include_router(users.router)
app.include_router(movies.router)
app.include_router(auth.router)
