from fastapi import FastAPI
from fastapi_practice.routers import authentication, blog, user, eventbrite
from fastapi_practice.cores.database import engine
from sqlmodel import SQLModel

app = FastAPI()

SQLModel.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(eventbrite.router)
