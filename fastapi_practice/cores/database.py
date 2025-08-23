from sqlmodel import Session, create_engine

SQLALCHAMY_DATABASE_URL = (
    "postgresql://postgres:Python&123Zee@localhost:5432/subhan"
)


engine = create_engine(SQLALCHAMY_DATABASE_URL, echo=True)


def get_db():
    with Session(engine) as session:
        yield session
