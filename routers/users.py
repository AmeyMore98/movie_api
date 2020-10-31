from typing import List

from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas import (
    user_schema,
)
from services import (
    auth_service, 
)
from handlers import (
    UserHandler
)
import constants
from routers import dependancies

router = APIRouter()

# User endpoints
@router.post("/users/", status_code=status.HTTP_201_CREATED, response_model=user_schema.User)
def create_user(
    new_user: user_schema.UserCreate, 
    db: Session = Depends(dependancies.get_db),
    user: user_schema.User = Depends(dependancies.get_current_user)
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

@router.get("/users/", response_model=List[user_schema.User])
def get_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(dependancies.get_db)
):
    """List all available users. 
    """
    users = UserHandler.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/users/{username}", response_model=user_schema.User)
def read_user(username: str, db: Session = Depends(dependancies.get_db)):
    user = UserHandler.get_user(db, username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=constants.RESOURCE_NOT_FOUND)
    return user

@router.put("/users/{username}", response_model=user_schema.User)
def update_user(
    username: str, 
    new_user: user_schema.UserUpdate,
    db: Session = Depends(dependancies.get_db),
    user: user_schema.User = Depends(dependancies.get_current_user)
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

@router.delete("/users/{username}", status_code=status.HTTP_200_OK)
def delete_user(
    username: str,
    db: Session = Depends(dependancies.get_db),
    user: user_schema.User = Depends(dependancies.get_current_user)
):
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=constants.OPERATION_NOT_PERMITTED)
    UserHandler.delete_user(db, username=username)
    return {constants.MESSAGE: constants.RESOURCE_DELETED}

