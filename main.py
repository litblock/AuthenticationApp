from sqlalchemy.orm import Session
import fastapi
from passlib.context import CryptContext

import database
from database import SessionLocal, engine, Base
from settings import KEY


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = fastapi.FastAPI()
Base.metadata.create_all(engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# SECRET_KEY = KEY
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/signup/")
async def create(user: database.UserCreate, db: Session = fastapi.Depends(get_db)):
    user = database.User(username=user.username, email=user.email, hashed_password=pwd_context.hash(user.password))
    db.add(user)
    return {"message": "User created", "username": user.username}
