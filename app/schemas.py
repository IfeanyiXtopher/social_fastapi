from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):    #schema/Pydantic Model is what its called... We are defining what we expect from our users.
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email:EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:           #This id from docmentation. to convert our response obj to dict
        # orm_mode = True   ## Outdated new is from_attributes
        from_attributes = True


class PostBase(BaseModel): 
    title: str
    content: str
    published: bool = True
    

class PostCreate(PostBase): #this means we are inheriting everything just as it is in Postbase
    pass 

class Post(PostBase): #Note that you only need to define the fields you need for response.. Also notice i inherited PostBase just to get its properties. thats if you need them .. you can just use your BaseModel and define only what you wish to send back to user 
    id: int
    owner_id:int
    created_at: datetime
    owner: UserOut

    class Config:           #This id from docmentation. to convert our response obj to dict
        from_attributes = True
        # orm_mode = True       ##Outdated new is from_attributes

class PostWithVotes(BaseModel):
    Post: Post
    votes:int


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

from pydantic import BaseModel, Field, validator

class Vote(BaseModel):
    post_id: int
    dir: int

    @validator('dir')           ## This function i created is to make sure dir only accpts 1 and 0
    def validate_dir(cls, v):
        if v not in {0, 1}:
            raise ValueError('Direction must be either 0 or 1')
        return v