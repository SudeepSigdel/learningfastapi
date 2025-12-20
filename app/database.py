from sqlmodel import create_engine, Session, SQLModel
from typing import Annotated
from fastapi import Depends, APIRouter

router = APIRouter()

DATABASE_URL = "postgresql://postgres:password@localhost/fastapi"

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

SessionLocal = Annotated[Session, Depends(get_session)]

def create_table_and_db():
    SQLModel.metadata.create_all(engine)

@router.on_event("startup")
def on_startup():
    create_table_and_db()