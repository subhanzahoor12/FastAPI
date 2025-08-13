from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from fastapi_practice.cores.redis1 import get_from_redis, set_from_db_to_redis
from fastapi_practice.cores import models, schemas
from fastapi_practice.cores.schemas import BlogResponse
from fastapi.encoders import jsonable_encoder


# def get_all(page_num: int = 1,page_size : int =10,db: Session):
#     start = (page_num - 1) * page_size
#     end = start + page_size 
#     blogs = db.query(models.Blog).all()
#     return blogs[start:end]
    # cached = get_from_redis("blogs")
    # if cached:
    #     return cached
    # else:
    #     blogs = db.query(models.Blog).all()
    #     blogs_list = [
    #         BlogResponse(**{k: v for k, v in blog.__dict__.items()})
    #         for blog in blogs
    #     ]
    #     set_from_db_to_redis("blogs", jsonable_encoder(blogs_list))
    #     return blogs


def create(request: schemas.ShowBlog, db: Session):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def destroy(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id : {id} is not availaible",
        )
    blog.delete(synchronize_session=False)
    db.commit()
    return "done"


def update(id: int, request: schemas.ShowBlog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"blog with id {id} not found",
        )
    blog.update(request.dict())
    db.commit()
    return "updated"


def show(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id : {id} is not availaible",
        )
    return blog
