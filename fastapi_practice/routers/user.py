from fastapi import APIRouter, Depends,status
from sqlmodel import Session
from fastapi import File, UploadFile
from fastapi_practice.cores import oauth2
from fastapi_practice.cores import database, models
from fastapi_practice.repository import user
from fastapi_practice.cores.models import User
from fastapi_practice.cores.oauth2 import get_current_user
from fastapi_practice.cores.minio_client import minio_client
import os
from fastapi_practice.repository.user import upload_profile_image


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

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_data(
    id: int,
    request: models.UserUpdate,
    db: Session = Depends(get_db),
):
    return user.update(id, request, db)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(
    id: int,
    db: Session = Depends(get_db),
):
    return user.destroy(id, db)

@router.post("/upload-profile-pic")
async def upload_image(
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
    user=Depends(get_current_user), 
):
    return await upload_profile_image(db, file, user)
