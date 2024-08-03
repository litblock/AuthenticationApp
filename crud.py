from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import Uuid
from sqlalchemy.orm import Session
import database
from passlib.context import CryptContext
from settings import KEY
import schemas
import uuid

SECRET_KEY = KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user_by_id(session: Session, id: uuid.UUID):
    return session.query(database.User).filter(database.User.id == id).first()


def get_user_by_username(session: Session, username: str):
    return session.query(database.User).filter(database.User.username == username).first()


def get_user_by_email(session: Session, email: str):
    return session.query(database.User).filter(database.User.email == email).first()


def get_id_by_username(session: Session, username: str):
    return session.query(database.User.id).filter(database.User.username == username).first()


def create_user(session: Session, user: schemas.UserCreate):
    db_user = database.User(id=uuid.uuid4(), username=user.username, email=user.email,
                            hashed_password=pwd_context.hash(user.password))
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def authenticate_user(session: Session, email: str, password: str):
    user = get_user_by_email(session, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def createToken():
    pass
