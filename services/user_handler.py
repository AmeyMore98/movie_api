from models import user_model

class UserHandler:

    @staticmethod
    def get_user(db, username: str):
        return db.query(user_model.User).filter_by(username=username).first()
