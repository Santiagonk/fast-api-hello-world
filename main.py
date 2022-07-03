#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel, ColorError, EmailStr, HttpUrl, PaymentCardNumber
from pydantic import Field

# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body, Query, Path, Form, Header, Cookie, UploadFile, File

app = FastAPI()

# Models

class HairColor(Enum):
    white: "white"
    brown: "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel):
    city: str = Field(
        ..., 
        min_length=1,
        max_length=50
        )
    state: str = Field(
        ..., 
        min_length=1,
        max_length=50
        )
    country: str = Field(
        ..., 
        min_length=1,
        max_length=50
        )

class PersonBase(BaseModel):
    first_name: str = Field(
        ..., 
        min_length=1,
        max_length=50,
        example="Africa"
        )
    last_name: str = Field(
        ..., 
        min_length=1,
        max_length=50,
        example="Aurelio"
        )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=5
        )
    hair_color: Optional[HairColor] = Field(default=None, example=HairColor.black)
    is_married: Optional[bool] = Field(default=None,example=True)

class Person(PersonBase):    
    password: str = Field(
        ..., 
        min_length=8,
        example="contrasenasegura"
        )

class PersonOut(PersonBase):
    pass

class LoginOut(BaseModel):
    username: str = Field(
        ..., 
        min_length=1,
        max_length=50,
        example="Africa"
        )
    message: str = Field(default="Login Succesfully!")

@app.get(
    path="/", 
    status_code=status.HTTP_200_OK
    )
def home():
    return {"Hello": "World"}

# Request and Response Body

@app.post(
    path="/person/new", 
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED
    )
def create_person(person: Person = Body(...)):
    return person

# Validaciones: Query Parameters

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK
    )
def show_person(
    name: Optional[str] = Query(
        None, min_length=1, 
        max_length=50,
        title="Person Name",
        description= "This is the person name. It's between 1 and 50 characters",
        example="Santiago"
        ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person Age, It's requiered",
        example=28
        )
    ):
    return {name: age}

# Validaciones: Path Parameters

@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK
    )
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

@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_200_OK
    )
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="Thi is the person ID",
        gt=0,
        example=123
    ),
    person: Person = Body(...),
    # location: Location = Body(...)  
    ):
    result = person.dict()
    # result.update(location.dict())
    return result

# Forms 

@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK
)
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username=username)

# Cookies and Headers Parameters

@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1
        ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1
        ),
    email: EmailStr = Form(...),    
    message: str = Form(
        ...,
        min_length=20
        ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)    
):
    return user_agent

# Files

@app.post(
    path="/post-image"
)
def post_image(
    image: UploadFile = File(...)
):
    return {
        "Filename":image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024,ndigits=2)
    }
