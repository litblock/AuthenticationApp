import uuid
from contextlib import asynccontextmanager
from urllib.request import Request

from fastapi.exceptions import RequestValidationError
from sqlalchemy import Uuid
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, FastAPI

from sqlalchemy.orm import Session
import fastapi
from starlette.responses import JSONResponse

import auth
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


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        errors.append({
            "loc": error["loc"],
            "msg": error["msg"],
            "type": error["type"]
        })
    return JSONResponse(
        status_code=422,
        content={
            "detail": errors
        }
    )


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/signup/", status_code=201, response_model=schemas.UserOut)
async def create(user: schemas.UserCreate, db: Session = fastapi.Depends(get_db)):
    try:
        return crud.create_user(db, user)
    except SQLAlchemyError as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Database error")


@app.post("/users/{identifier}", response_model=schemas.UserOut)
async def get_user(identifier: Union[uuid.UUID, str], db: Session = fastapi.Depends(get_db)):
    if isinstance(identifier, uuid.UUID):
        db_user = crud.get_user_by_id(db, id=identifier)
    else:
        db_user = crud.get_user_by_username(db, username=identifier)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/login")
async def login(user: schemas.UserLogin, db: Session = fastapi.Depends(get_db)):
    user = auth.authenticate_user(db, email=user.email, password=user.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth.create_access_token(data={"sub": user.email})
    return "Success", schemas.UserLoginSuccess(username=user.username, email=user.email, access_token=token)


@app.get("/users/me")
async def me():
    return "signed in"
