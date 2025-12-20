from sqlmodel import SQLModel, Column, TIMESTAMP, ForeignKey, Relationship, Field, Integer
from pydantic import EmailStr
from datetime import datetime

class UserBase(SQLModel):
    email: EmailStr = Field(unique= True)
    password: str

class User(UserBase, table=True):
    __tablename__= "users" #type: ignore
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default_factory= datetime.utcnow, sa_column=Column(TIMESTAMP(timezone=True)))

class UserCreate(UserBase):
    pass

class UserResponse(SQLModel):
    id: int
    email: EmailStr
    created_at: datetime


class PostBase(SQLModel):
    title: str
    content: str
    published: bool | None = True

class Post(PostBase, table=True):
    __tablename__ = "posts" #type: ignore

    id: int | None = Field(default= None, primary_key= True)
    created_at: datetime | None = Field(default_factory=datetime.utcnow, sa_column=Column(TIMESTAMP(timezone=True), nullable= False))
    owner_id: int = Field(sa_column=Column(Integer, ForeignKey("users.id", ondelete="CASCADE")))
    owner: User = Relationship()

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id : int
    owner: UserResponse



class Token(SQLModel):
    access_token : str
    token_type : str

class TokenData(SQLModel):
    id : int