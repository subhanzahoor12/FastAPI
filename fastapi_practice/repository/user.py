from fastapi import HTTPException, status, Depends, UploadFile, File
from fastapi.encoders import jsonable_encoder
from sqlmodel import Session, select
from fastapi_practice.cores.models import User
from pathlib import Path
from fastapi_practice.cores.oauth2 import get_current_user
from fastapi_practice.cores import models
from fastapi_practice.cores.hashing import Hash
from fastapi_practice.cores.redis1 import get_from_redis, set_from_db_to_redis
from fastapi_practice.cores.minio_client import minio_client
import os

async def upload_profile_image(
    db: Session ,
    file: UploadFile ,
    user=Depends(),
):
    bucket_name = "images"

    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)

    file_extension = os.path.splitext(file.filename)[1]
    object_name = f"image_{os.urandom(8).hex()}{file_extension}"

    try:
        minio_client.put_object(
            bucket_name,
            object_name,
            file.file,
            length=-1,
            part_size=10 * 1024 * 1024,
        )

        # save path in DB
        image_path = f"/{bucket_name}/{object_name}"
        setattr(user, "picture_path", image_path)
        db.add(user)
        db.commit()
        db.refresh(user)

        return {"message": "Image uploaded successfully", "path": image_path}

    except Exception as e:
        return {"message": f"Error uploading image: {e}"}


def create(request: models.User, db: Session):
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
    user = db.get(models.User, id)
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
        users = db.exec(select(models.User)).all()
        users_list = [
            models.User(**{k: v for k, v in user.__dict__.items()})
            for user in users
        ]
        set_from_db_to_redis("users", jsonable_encoder(users_list))

        return users

def update(id: int, request: models.UserUpdate, db: Session):
    user = db.get(models.User, id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"blog with id {id} not found",
        )
    update_data = request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)

    db.add(user)
    db.commit()
    db.refresh(user)
    return {"detail": f"user {id} updated successfully!"}

def destroy(id: int, db: Session):
    user = db.get(models.User, id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id : {id} is not availaible",
        )
    db.delete(user)
    db.commit()
    return user