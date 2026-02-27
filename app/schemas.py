# Defines Pydantic models for request/response validation.

from pydantic import BaseModel, Field, EmailStr

class UserRequest(BaseModel):
    username : str
    email : EmailStr
    first_name : str
    last_name : str
    hash_password : str
    role: str




class Token(BaseModel):
    access_token : str
    token_type: str


class TodoRequest(BaseModel):
    title : str = Field(..., max_length=256)
    description : str = Field(..., max_length=512)
    priority : int = Field(...)
    completed : bool


class Password_Change(BaseModel):
    password : str
    new_password : str = Field(min_length=6)