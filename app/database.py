from sqlmodel import create_engine, Session, SQLModel
from typing import Annotated
from fastapi import Depends#, APIRouter
from .config import setting

# router = APIRouter()

DATABASE_URL = f"postgresql://{setting.database_username}:{setting.database_password}@{setting.database_host}:{setting.database_port}/{setting.database_name}"

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

SessionLocal = Annotated[Session, Depends(get_session)]

# def create_db_and_table():
#     SQLModel.metadata.create_all(engine)

# @router.on_event("startup")
# def on_startup():
#     create_db_and_table()