from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

import fastapi

app = fastapi.FastAPI()

app.route("/home")


def home():
    return {"message": "Home"}


app.post("/users/{id}")


def login():
    return {"message": "Login"}
