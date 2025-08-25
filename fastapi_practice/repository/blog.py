from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlmodel import Session, select
from fastapi_practice.cores.models import Blog
from fastapi_practice.cores.redis1 import get_from_redis, set_from_db_to_redis


def get_all(request: Blog, db: Session, page_num: int = 1, page_size: int = 10):
    start = (page_num - 1) * page_size
    end = start + page_size
    conditions = []
    request = dict(request)
    for key, value in request.items():
        if value is not None:
            blog_column = getattr(Blog, key, None)
            conditions.append(blog_column.ilike(f"%{value}%"))
    blogs = db.exec(select(Blog).filter(*conditions))
    blogs = blogs.all()
    blogs_length = len(blogs)
    response = {
        "blogs": blogs[start:end],
        "total": blogs_length,
        "count": page_size,
        "pagination": {},
    }
    if end >= blogs_length:
        response["pagination"]["next"] = None
        if page_num > 1:
            response["pagination"]["previous"] = (
                f"/blog/?page_num = {page_num - 1}&page_size= {page_size}"
            )
        else:
            response["pagination"]["previous"] = None
    else:
        if page_num > 1:
            response["pagination"]["previous"] = (
                f"/blog/?page_num = {page_num - 1}&page_size= {page_size}"
            )
        else:
            response["pagination"]["previous"] = None
        response["pagination"]["next"] = (
            f"/blog/?page_num = {page_num + 1}&page_size= {page_size}"
        )
    return response
    # cached = get_from_redis("blogs")
    # if cached:
    #     return cached
    # else:
    #     blogs = db.query(Blog).all()
    #     blogs_list = [
    #         Blog(**{k: v for k, v in blog.__dict__.items()}) for blog in blogs
    #     ]
    #     set_from_db_to_redis("blogs", jsonable_encoder(blogs_list))
    #     return blogs


def create(request: Blog, db: Session):
    db.add(request)
    db.commit()
    db.refresh(request)
    return request


def destroy(id: int, db: Session):
    blog = db.get(Blog, id)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id : {id} is not availaible",
        )
    db.delete(blog)
    db.commit()
    return blog


def update(id: int, request: Blog, db: Session):
    blog = db.get(Blog, id)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"blog with id {id} not found",
        )
    update_data = request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(blog, key, value)
    db.add(blog)
    db.commit()
    return "updated"


def show(id: int, db: Session):
    blog = db.get(Blog, id)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id : {id} is not availaible",
        )
    return blog
