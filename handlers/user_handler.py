from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import user_model
from schemas import user_schema

class UserHandler:

    @staticmethod
    def get_user(db, username: str):
        return db.query(user_model.User).filter_by(username=username).first()

    @staticmethod
    def create_user(db: Session, user: user_schema.UserCreate):
        user = user.dict()
        user['hashed_password'] = user['password']
        del user['password']
        print(user)
        db_user = user_model.User(**user)
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
        
        user = user.dict()
        user['hashed_password'] = user['password']
        del user['password']
        for key, value in user.items():
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
