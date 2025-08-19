from sqlmodel import create_engine,Session

SQLALCHAMY_DATABASE_URL = "sqlite:///./blog.db"


engine = create_engine(
    SQLALCHAMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

def get_db():
    with Session(engine) as session:
        yield session
