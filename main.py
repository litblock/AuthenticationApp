from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session

import fastapi

app = fastapi.FastAPI()


class Data(BaseModel):
    name: str
    age: int


@app.post("/create/")
async def create(data: Data):
    return {"name": data.name, "age": data.age}


@app.get("/test/{item_id}/")
async def test(item_id: str, q: int = 5):
    return {"message": item_id, "q": q}
