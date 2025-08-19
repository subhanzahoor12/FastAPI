from sqlmodel import SQLModel,Field,Relationship
from typing import List
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str
    name: str
    password: str
    blogs: List["Blog"] = Relationship(back_populates="creator")
class Blog(SQLModel,table = True):
    id: int | None = Field(default=None,primary_key=True)
    title: str
    body: str
    user_id: int | None = Field(default = None,foreign_key="user.id")
    creator : User =Relationship(back_populates= "blogs")

