from sqlalchemy import (
    Column,
    String, 
    Boolean
)

from db.database import Base

class User(Base):
    __tablename__ = 'users'

    username = Column(String, primary_key=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False)
