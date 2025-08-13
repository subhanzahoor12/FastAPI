from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi_practice.cores import models, schemas
from fastapi_practice.cores.hashing import Hash
from fastapi_practice.cores.redis1 import get_from_redis, set_from_db_to_redis
from fastapi_practice.cores.schemas import ShowUser


def create(request: schemas.ShowBlog, db: Session):
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=Hash.bcrypt(request.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def show(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id {id} is not available",
        )
    return user

def show_all(db: Session):
    cached = get_from_redis("users")
    if cached:
        return cached
    else:
        users = db.query(models.User).all()
        users_list = [
            ShowUser(**{k: v for k, v in user.__dict__.items()})
            for user in users
        ]
        set_from_db_to_redis("users", jsonable_encoder(users_list))

        return users

