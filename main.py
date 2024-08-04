import uuid
from contextlib import asynccontextmanager
from urllib.request import Request

from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import Uuid
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, FastAPI, Depends

from sqlalchemy.orm import Session
import fastapi
from starlette import status
from starlette.responses import JSONResponse
from settings import oauth2_scheme
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
async def create(user: schemas.UserCreate, db: Session = fastapi.Depends(database.get_db)):
    try:
        return crud.create_user(db, user)
    except SQLAlchemyError as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Database error")


@app.post("/users/{identifier}", response_model=schemas.UserOut)
async def get_user(identifier: Union[uuid.UUID, str], db: Session = fastapi.Depends(database.get_db)):
    if isinstance(identifier, uuid.UUID):
        db_user = crud.get_user_by_id(db, id=identifier)
    else:
        db_user = crud.get_user_by_username(db, username=identifier)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = auth.authenticate_user(db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/users/me/", response_model=schemas.UserOut)
async def read_users_me(current_user: schemas.UserOut = Depends(auth.get_current_user)):
    return current_user
