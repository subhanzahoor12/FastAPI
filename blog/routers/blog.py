from fastapi import APIRouter,Depends
from .. import schemas,database,models
from typing import List
from sqlalchemy.orm import Session
router = APIRouter()





@router.get("/blog", response_model=list[schemas.ShowBlog], tags=["blogs"])
def all(db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).all()
    return blog