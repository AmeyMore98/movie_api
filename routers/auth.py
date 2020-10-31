from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from schemas import token_schema
from services import (
    auth_service, 
    jwt_service
)
import constants
from routers import (
    dependancies
)


router = APIRouter()

# Authentication endpoints
@router.post("/login", response_model=token_schema.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(dependancies.get_db)
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
