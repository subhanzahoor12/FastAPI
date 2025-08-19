from fastapi import APIRouter, Depends
from sqlmodel import Session

from fastapi_practice.cores import database, models
from fastapi_practice.repository import user

router = APIRouter(prefix="/user", tags=["Users"])
get_db = database.get_db


@router.post("/", response_model=models.User)
def create_user(request: models.User, db: Session = Depends(get_db)):
    return user.create(request, db)


@router.get("/{id}", response_model=models.User)
def get_user(id: int, db: Session = Depends(get_db)):
    return user.show(id, db)

@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return user.show_all(db)