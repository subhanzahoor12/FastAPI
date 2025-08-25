from sqlmodel import Session, create_engine
from fastapi_practice.cores.config import DB_URL

SQLALCHAMY_DATABASE_URL = (DB_URL)


engine = create_engine(SQLALCHAMY_DATABASE_URL, echo=True)


def get_db():
    with Session(engine) as session:
        yield session
