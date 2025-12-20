from pydantic import EmailStr
from sqlmodel import SQLModel, Field, TIMESTAMP, Column, String, text
from datetime import datetime

class PostBase(SQLModel):
    title: str
    content: str
    published: bool | None = Field(default=True)

class Post(PostBase, table=True):
    __tablename__ = "posts" # type: ignore
    id: int | None = Field(default= None, primary_key=True)
    created_at: datetime | None = Field(default_factory=datetime.utcnow, sa_column=Column(TIMESTAMP(timezone=True), nullable=False))

class CreatePost(PostBase):
    pass

class UpdatePost(PostBase):
    pass

class PatchPost(SQLModel):
    title: str | None = None
    content: str | None = None
    published: bool | None = None

class PostResponse(PostBase):
    id: int
    created_at: datetime


class UserBase(SQLModel):
    email: EmailStr= Field(sa_column=Column(String,nullable=False, unique= True))
    password: str

class User(UserBase, table=True):
    __tablename__="users" # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default_factory=datetime.utcnow, sa_column=Column(TIMESTAMP(timezone=True), server_default=text("now()")))

class UserCreate(UserBase):
    pass

class UserResponse(SQLModel):
    id: int
    email: EmailStr
    created_at: datetime

class UserLogin(UserBase):
    pass