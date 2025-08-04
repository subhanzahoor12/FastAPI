from fastapi import FastAPI
from typing import Optional

app = FastAPI()


@app.get('/blog')
def index(limit = 12 , published : bool = True,sort : Optional[str] = None):
    if published:
        return {"data": f"{limit} published blogs from the db"}
    else:
        return {'data': f"{limit} blogs from the db"}

@app.get("/blog/unpublished")
def unpublished():
    return {"data": "all blogs are unpublished"}

@app.get('/blog/{id}')
def about(id:int):
    return {'data': id}

@app.get('/blog/{id}/comments')
def comments(id):
    return {'data':{'1','2'}}
 
@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'all blogs are unpublished'}