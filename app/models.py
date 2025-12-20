from sqlmodel import SQLModel, Field, BOOLEAN, Column, TIMESTAMP, text
from datetime import datetime

class PostBase(SQLModel):
    title: str
    content: str
    published: bool | None = Field(default= True, sa_column= Column(BOOLEAN, nullable= False, server_default="True"))

class Post(PostBase, table=True):
    __tablename__ = "posts" # type: ignore
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory= datetime.utcnow ,sa_column=Column(TIMESTAMP(timezone=True), nullable=False))

class CreatePost(PostBase):
    pass

class UpdatePost(PostBase):
    pass


class ReadPost(PostBase):
    id:  int
    created_at: datetime

class PatchPost(SQLModel):
    title: str | None = None
    content: str | None = None
    published: bool | None = None