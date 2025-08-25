from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from fastapi_practice.cores import database, models, oauth2
from fastapi_practice.repository import blog

router = APIRouter(prefix="/blog", tags=["Blogs"])

get_db = database.get_db


@router.get("/")
def get_all(
    request: models.Blog = Depends(),
    db: Session = Depends(get_db),
    page_num: int = 1,
    page_size: int = 10,
):
    return blog.get_all(request,db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(
    request: models.Blog,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    return blog.create(request, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    return blog.destroy(id, db)


@router.get("/{id}", status_code=200, response_model=models.Blog)
def get_one(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    return blog.show(id, db)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_data(
    id: int,
    request: models.Blog,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    return blog.update(id, request, db)
