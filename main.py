from fastapi import FastAPI

from fastapi_practice.cores import models
from fastapi_practice.cores.database import engine
from fastapi_practice.routers import authentication, blog, user

app = FastAPI()

# models.Base.metadata.drop_all(engine)
models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)
