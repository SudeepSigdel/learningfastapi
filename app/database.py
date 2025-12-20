from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine
from typing import Annotated

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session


SessionLocal = Annotated[Session, Depends(get_session)]

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)