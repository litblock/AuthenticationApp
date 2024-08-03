from sqlalchemy.orm import Session
import database


def get_user_by_id(session: Session, id: int):
    return session.query(database.User).filter(database.User.id == id).one()


def get_user_by_username(session: Session, username: str):
    return session.query(database.User).filter(database.User.username == username).one()


def get_user_by_email(session: Session, email: str):
    return session.query(database.User).filter(database.User.email == email).one()


def create_user(session: Session, user: database.UserCreate):
    db_user = database.User(username=user.username, email=user.email, hashed_password=user.password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
