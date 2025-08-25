from sqlmodel import Session, create_engine
from fastapi_practice.cores.config import db_url

SQLALCHAMY_DATABASE_URL = (db_url)


engine = create_engine(SQLALCHAMY_DATABASE_URL, echo=True)


def get_db():
    with Session(engine) as session:
        yield session
