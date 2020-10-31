from passlib.context import CryptContext

from handlers.user_handler import UserHandler

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Service to handle user authentication.
    """
    
    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return pwd_context.hash(password)

    def authenticate_user(self, db, username: str, password: str):
        user = UserHandler.get_user(db, username)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user
