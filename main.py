from doctest import Example
from fastapi import FastAPI, Body, Form, Path, Query, status
from pydantic import BaseModel, Field, EmailStr, HttpUrl, create_model
from typing import Optional
from enum import Enum
app = FastAPI()

# Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class _Person(BaseModel):
    password: str = Field(..., min_length=8, max_length=100,example="password")

class Person(BaseModel):
    first_name: str = Field(...,min_length=1,max_length=24, example="Facundo")
    last_name: str = Field(...,min_length=1,max_length=24, example="Veronelli")
    age: int = Field(...,ge=18, example="22")
    email: EmailStr = Field(...,example="facu@test.com")
    blog: HttpUrl = Field(..., example="https://www.facu.com")

    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default = False)

class Person_(Person,_Person):
    pass

class Location(BaseModel):
    city: str = Field(min_length=4, example="VDP")
    state: str = Field(...,min_length=4, example ="CABA")
    country: str = Field(...,max_length=10, example="ARG")

class LoginOut(BaseModel):
    username: str = Field(...,max_length=20,example="Facundo")


@app.get(path="/",status_code=status.HTTP_200_OK)
def home():
    return {"message":"Hello World"}

# Request and Response Body
@app.post(path="/person/new",response_model=Person,status_code=status.HTTP_201_CREATED)
def create_person(person:Person_ = Body(...)):
    return person


# Validaciones: Query parameters

@app.get(path="/person/detail", status_code=status.HTTP_200_OK)
def show_person(
    name:Optional[str] = Query(
        None,
        min_length=1,
        max_length=24,
        title="Person Name",
        description="This is the person name it's between 1 to 24 characters",
        example="Facundo",
        ),

        age: Optional[int] = Query(
            ...,
            example=22,
            title="Person age",
            description="This is the person age, it's requied parameter"
            )
    ):
    return {name:age}

# Validaciones: Path Parameters

@app.get(path="/person/detail/{person_id}", status_code=status.HTTP_302_FOUND)
def show_person(person_id: int = Path(...,gt=0,example=3)):
    return {person_id:"exits"}


# Validaciones: Request Body

@app.put(path="/person/{person_id}", status_code=status.HTTP_202_ACCEPTED)
def update_person(
    person_id:int = Path(
        ...,
        title = "person id",
        description = "this is the person id",
        gt = 0,
        example=1
        ),
        person: Person = Body(...),
        location: Location = Body(...)
        ):
    results = person.dict()
    results.update(location.dict())

    return results

@app.post(path="/login",response_model=LoginOut,status_code=status.HTTP_200_OK)
def login(username: str = Form(...),password: str = Form(...)):
    return LoginOut(username=username)
