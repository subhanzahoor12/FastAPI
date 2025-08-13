from typing import List, Optional

from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    body: str
    
    model_config = {"from_attributes": True}




class User(BaseModel):
    name: str
    email: str
    password: str



class ShowBlog(BaseModel):
    title: str
    body: str

    model_config = {"from_attributes": True}


class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[ShowBlog] = []

    model_config = {"from_attributes": True}    


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class BlogResponse(BaseModel):
    id: int
    title: str
    body: str

    
