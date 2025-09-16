import datetime
from typing import List

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str
    name: str
    password: str
    picture_path: str | None = None  
    blogs: List["Blog"] = Relationship(back_populates="creator")

class UserCreate(SQLModel):
    email: str
    name: str
    password: str


class Blog(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    body: str
    user_id: int | None = Field(default=None, foreign_key="user.id")
    creator: User = Relationship(back_populates="blogs")


class Login(SQLModel):
    username: str
    password: str


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    email: str | None = None


class EventData(SQLModel):
    name: str
    start: str
    end: str
    currency: str | None = Field(default="USD")


class UserUpdate(SQLModel):
    email: str | None = None
    name: str | None = None
    password: str | None = None


class Chat(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")  
    receiver_id: int = Field(foreign_key="user.id") 
    message: str
    timestamp: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow
    )
