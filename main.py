#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
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

# Endpoints

@app.get(
    path="/", 
    status_code=status.HTTP_200_OK
    )
def home():
    """
    Home page of the API

    This path returns the home page of the API.

    No parameters are required.
    """
    return {"Hello": "World"}

# Request and Response Body

@app.post(
    path="/person/new", 
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"],
    summary="Create Person in the app"
    )
def create_person(person: Person = Body(...)):
    """
    Create Person

    This path operation creates a person in the app and save the information in the database

    Parameters:
    - Request body parameter:
        - **person: Person** -> A person model with first name, last name, age, hair color and is married
    
    Returns a person model with first name, last name, age, hair color and marital status
    """
    return person

# Validaciones: Query Parameters


@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags=["Persons"],
    deprecated=True
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
    """
    Show Person

    This path operation shows the person's name and age in the app from the database.

    Parameters:
    - Query parameter:
        - **name: str** -> This is the person name. It's between 1 and 50 characters.
        - **age: int** -> This is the person age. It's required.

    Returns a JSON with the person's name and age.
    """
    return {name: age}

# Validaciones: Path Parameters

persons = [1, 2, 3, 4, 5]

@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
    )
def show_person(
    person_id: int = Path(
        ..., 
        gt = 0,
        title="Person id",
        description="This is the person id, It's requiered"
        )
    ):
    """
    Show Person

    This path operation shows the person's ID in the app from the database.

    Parameters:
    - Path parameter:
        - **person_id: int** -> This is the person ID. It's required and must be greater than 0.

    Returns a JSON with the person's ID.
    """
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡This person doesn't exist!"
        )
    return {person_id: "It exists!"}

# Validaciones: Request Body

@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
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
    """
    Update Person

    This path operation updates the person's information from the database.

    Parameters:
    - Path parameter:
        - **person_id: int** -> This is the person ID. It's required and must be greater than 0.
    - Request body parameter:
        - **person: Person** -> A person model with first name, last name, age, hair color, is married, email, payment card number, favorite color and password.
        - **location: Location** -> A location model with city, state and country.

    Returns a JSON with the person's ID, its model and location.
    """
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
    """
    User login

    This path operation allows you to login in the app.

    Parameters:
    - Request body parameter:
        - **username: str** -> This is the username to enter in the form. It's required.
        - **password: str** -> This is the password to enter in the form. It's required.

    Returns a JSON with the username and a message.
    """
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
    """
    Contact

    This path operation allows the user to contact the company.

    Parameters:
    - user_agent: The browser that the user is using.
    - ads: The cookies that this website uses.
    - Request body parameter:
        - **first_name: str** -> This is the first name to enter in the form. It's required.
        - **last_name: str** -> This is the last name to enter in the form. It's required.
        - **email: EmailStr** -> This is the email to enter in the form. It's required.
        - **message: str** -> This is the message to enter in the form. It's required.

    """
    return user_agent

# Files

@app.post(
    path="/post-image"
)
def post_image(
    image: UploadFile = File(...)
):
    """
    Post image

    This path operation allows you to post an image in the app to the database.

    Parameters:
    - Request body parameter:
        - **image: UploadFile** -> This is the image to upload. It's required.

    Returns a JSON with the image's name, format and size in kb.
    """
    return {
        "Filename":image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024,ndigits=2)
    }
