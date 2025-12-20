from pydantic import EmailStr
from sqlmodel import TIMESTAMP, Column, SQLModel, Field, String, text, Integer, ForeignKey, Relationship
from datetime import datetime
from typing import Optional

class UserBase(SQLModel):
    email: EmailStr = Field(sa_column=Column(String, unique=True))
    password: str = Field(nullable=False)

class User(UserBase, table=True):
    __tablename__ = "users" # type: ignore
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default_factory=datetime.utcnow, sa_column=Column(TIMESTAMP(timezone=True), server_default=text("now()")))

class UserCreate(UserBase):
    pass

class UserResponse(SQLModel):
    id: int
    email: EmailStr
    created_at: datetime

class Token(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    id: Optional[int]= None

class PostBase(SQLModel):
    title: str
    content: str
    published: bool | None = True

class Post(PostBase, table=True):
    __tablename__="posts" # type: ignore
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default_factory=datetime.utcnow, sa_column=Column(TIMESTAMP(timezone=True), server_default=text("now()")))
    owner_id : int = Field(sa_column=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False))
    owner : User =Relationship()

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id : int
    owner: UserResponse  # type: ignore