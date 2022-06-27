#Python
from email.policy import default
import imp
import re
from typing import Optional
from unittest import result

#Pydantic
from pydantic import BaseModel

# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

# Models

class Location(BaseModel):
    city: str
    state: str
    country: str

class Person(BaseModel):
    first_name: str 
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None
    

@app.get("/")
def home():
    return {"Hello": "World"}

# Request and Response Body

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

# Validaciones: Query Parameters

@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None, min_length=1, 
        max_length=50,
        title="Person Name",
        description= "This is the person name. It's between 1 and 50 characters"
        ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person Age, It's requiered"
        )
    ):
    return {name: age}

# Validaciones: Path Parameters

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ..., 
        gt = 0,
        title="Person id",
        description="This is the person id, It's requiered"
        )
    ):
    return {person_id: "It exists!"}

# Validaciones: Request Body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="Thi is the person ID",
        gt=0
    ),
    person: Person = Body(...),
    location: Location = Body(...)  
    ):
    result = person.dict()
    result.update(location.dict())
    return result
