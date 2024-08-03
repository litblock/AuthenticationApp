from sqlalchemy.orm import Session
import database
from passlib.context import CryptContext

import schemas
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_id(session: Session, id: int):
    return session.query(database.User).filter(database.User.id == id).first()


def get_user_by_username(session: Session, username: str):
    return session.query(database.User).filter(database.User.username == username).first()


def get_user_by_email(session: Session, email: str):
    return session.query(database.User).filter(database.User.email == email).first()


def create_user(session: Session, user: schemas.UserCreate):
    db_user = database.User(id=uuid.uuid4(), username=user.username, email=user.email, hashed_password=pwd_context.hash(user.password))
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
