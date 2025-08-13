from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fastapi_practice.cores import database, schemas
from fastapi_practice.repository import user

router = APIRouter(prefix="/user", tags=["Users"])
get_db = database.get_db


@router.post("/", response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(request, db)


@router.get("/{id}", response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    return user.show(id, db)

@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return user.show_all(db)