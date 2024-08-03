import uuid
from contextlib import asynccontextmanager

from sqlalchemy import Uuid
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, FastAPI

from sqlalchemy.orm import Session
import fastapi

import crud
import database
import schemas
from database import SessionLocal, engine, Base
from settings import KEY
from typing import Union


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_db()
    yield


app = FastAPI(lifespan=lifespan)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# SECRET_KEY = KEY
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/signup/", status_code=201, response_model=schemas.UserOut)
async def create(user: schemas.UserCreate, db: Session = fastapi.Depends(get_db)):
    try:
        db_user = crud.get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        return crud.create_user(db, user)
    except SQLAlchemyError as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Database error")


@app.get("/users/{identifier}", response_model=schemas.UserOut)
async def get_user(identifier: Union[uuid.UUID, str], db: Session = fastapi.Depends(get_db)):
    if isinstance(identifier, uuid.UUID):
        db_user = crud.get_user_by_id(db, id=identifier)
    else:
        db_user = crud.get_user_by_username(db, username=identifier)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/login")
async def login(user: schemas.UserLogin, db: Session = fastapi.Depends(get_db)):
    return {"message": "Login page"}
