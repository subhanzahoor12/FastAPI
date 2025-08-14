from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from fastapi_practice.cores import database, models, oauth2, schemas
from fastapi_practice.repository import blog

router = APIRouter(prefix="/blog", tags=["Blogs"])

get_db = database.get_db


@router.get("/")
def get_all(
    request: schemas.Blog = Depends(),
    db: Session = Depends(get_db),
    page_num: int = 1,
    page_size: int = 10,
):
    start = (page_num - 1) * page_size
    end = start + page_size
    conditions = []
    request = dict(request)
    for key, value in request.items():
        if value is not None:
            blog_column = getattr(models.Blog, key, None)
            conditions.append(blog_column.ilike(f"%{value}%"))
    blogs = db.query(models.Blog).filter(*conditions).all()
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


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(
    request: schemas.ShowBlog,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return blog.create(request, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return blog.destroy(id, db)


@router.get("/{id}", status_code=200, response_model=schemas.ShowBlog)
def get_one(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return blog.show(id, db)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_data(
    id: int,
    request: schemas.ShowBlog,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return blog.update(id, request, db)
