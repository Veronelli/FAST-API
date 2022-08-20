from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Models

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int

    hair_color: Optional[str]
    is_married: Optional[bool]

@app.get("/")
def home():
    return {"message":"Hello World"}

# Request and Response Body
@app.post("/person/new")
def create_person(person:Person = Body(...)):
    return person

