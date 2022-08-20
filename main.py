from fastapi import FastAPI, Body, Path, Query
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


# Validaciones: Query parameters

@app.get("/person/detail")
def show_person(
    name:Optional[str] = Query(
        None,
        min_length=1,
        max_length=24,
        title="Person Name",
        description="This is the person name it's between 1 to 24 characters"
        ),

        age: Optional[int] = Query(
            ...,
            title="Person age",
            description="This is the person age, it's requied parameter"
            )
    ):
    return {name:age}

# Validaciones: Path Parameters

@app.get("/person/detail/{person_id}")
def show_person(person_id: int = Path(...,gt=0)):
    return {person_id:"exits"}
