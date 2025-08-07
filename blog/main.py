from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas
from .database import SessionLocal, engine
from passlib.context import CryptContext
app = FastAPI()

# models.Base.metadata.drop_all(engine)
models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog", response_model=list[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    blog = db.query(models.Blog).all()
    return blog


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id : {id} is not availaible",
        )
    blog.delete(synchronize_session=False)
    db.commit()
    return "done"


@app.get("/blog/{id}", status_code=200, response_model=schemas.ShowBlog)
def get_one(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id : {id} is not availaible",
        )
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {'detail': f"Blog with id : {id} is not availaible"}

    return blog


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_data(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"blog with id {id} not found",
        )
    blog.update(request.dict())
    db.commit()
    return "updated"

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post('/user')
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    hashed_password = pwd_cxt.hash(request.email)
    new_user = models.User(
        name=request.name, email=request.email, password=hashed_password
        )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
