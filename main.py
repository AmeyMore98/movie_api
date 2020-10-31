from fastapi import FastAPI

from db.database import engine, Base
from routers import (
    users,
    movies,
    auth
)

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users.router)
app.include_router(movies.router)
app.include_router(auth.router)
