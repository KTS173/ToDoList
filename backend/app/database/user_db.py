from os import name

from sqlalchemy.orm import Session
from app.database.base import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCRUD:

    @staticmethod
    def create_user(db: Session, email: str, password: str):

        password = password[:72]

        hashed_password = pwd_context.hash(password)

        user = User(email=email, password=hashed_password, name=name)

        db.add(user)
        db.commit()
        db.refresh(user)

        return user


    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()