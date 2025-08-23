from typing import List

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str
    name: str
    password: str
    blogs: List["Blog"] = Relationship(back_populates="creator")


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
