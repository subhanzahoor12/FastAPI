from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from fastapi_practice.cores import database, oauth2, schemas
from fastapi_practice.repository import blog

router = APIRouter(prefix="/blog", tags=["Blogs"])

get_db = database.get_db


@router.get("/", response_model=list[schemas.ShowBlog])
def all(
    db: Session = Depends(get_db),
    # current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return blog.get_all(db)


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
