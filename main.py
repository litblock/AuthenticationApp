from contextlib import asynccontextmanager

from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, FastAPI

from sqlalchemy.orm import Session
import fastapi
from passlib.context import CryptContext

import crud
import database
from database import SessionLocal, engine, Base
from settings import KEY


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_db()
    yield


app = FastAPI(lifespan=lifespan)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# SECRET_KEY = KEY
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/signup/", status_code=201)
async def create(user: database.UserCreate, db: Session = fastapi.Depends(get_db)):
    return


def isValidUsername(db: Session, username: str):
    if len(username) < 3:
        return False
    elif crud.get_user_by_username(db, username) is not None:
        return False
    return True