from fastapi import HTTPException, status
from sqlmodel import Session,select
from fastapi_practice.cores.redis1 import get_from_redis, set_from_db_to_redis
from fastapi_practice.cores.models import Blog
from fastapi.encoders import jsonable_encoder


def get_all(db: Session,page_num: int = 1,page_size : int =10):
    start = (page_num - 1) * page_size
    end = start + page_size 
    blogs = db.exec(select(Blog)).all()
    return blogs[start:end]
    cached = get_from_redis("blogs")
    if cached:
        return cached
    else:
        blogs = db.query(Blog).all()
        blogs_list = [
            Blog(**{k: v for k, v in blog.__dict__.items()})
            for blog in blogs
        ]
        set_from_db_to_redis("blogs", jsonable_encoder(blogs_list))
        return blogs


def create(request : Blog, db: Session):
    db.add(request)
    db.commit()
    db.refresh(request)
    return request


def destroy(id: int, db: Session):
    blog = db.get(Blog,id)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id : {id} is not availaible",
        )
    db.delete(blog)
    db.commit()
    return blog


def update(id: int, request: Blog, db: Session):
    blog = db.get(Blog,id)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"blog with id {id} not found",
        )
    blog.title = request.title
    blog.body = request.title
    db.add(blog)
    db.commit()
    return "updated"


def show(id: int, db: Session):
    blog = db.get(Blog,id)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id : {id} is not availaible",
        )
    return blog
