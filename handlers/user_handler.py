from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import user_model
from schemas import user_schema

class UserHandler:

    @staticmethod
    def create_user(db: Session, user: user_schema.UserCreate):
        if UserHandler.get_user(db, user.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Resource already exisits"
            )
        db_user = user_model.User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_user(db: Session, username: str):
        return db.query(user_model.User).get(username)

    @staticmethod
    def update_user(db: Session, user: user_schema.UserUpdate, username: str):
        existing_user = db.query(user_model.User).get(username)
        if not existing_user:
            raise HTTPException(status_code=404, detail="Resource not found")
        
        for key, value in user.dict().items():
            setattr(existing_user, key, value)

        db.add(existing_user)
        db.commit()
        db.refresh(existing_user)
        return existing_user

    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100):
        return db.query(user_model.User).offset(skip).limit(limit).all()

    @staticmethod
    def delete_user(db: Session, username: str):
        user = db.query(user_model.User).get(username)
        if user:
            db.delete(user)
            db.commit()
            return 
        
        return
