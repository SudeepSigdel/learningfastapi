from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlmodel import select
from .database import create_db_and_tables, SessionLocal
from .models import Post, CreatePost
from . import models

app = FastAPI()

# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='password', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connection with Database Successful!")
        break
    except Exception as error:
        print("Connection with database failed!")
        print("Error:", error)
        time.sleep(2)


# This creartes db and tables on starting fastapi if they don't exist
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# This is just checking if our session was successfully implemented
@app.get("/status")
def status_db( db: SessionLocal):
    posts = db.exec(select(Post))
    return {"posts":posts}

@app.get("/")
def index():
    return{"Message":"DAY 2 of FastAPI"}

@app.get("/posts")
def get_all_posts(db: SessionLocal):
    # cursor.execute("""SELECT * FROM posts;""")
    # posts = cursor.fetchall()
    posts = db.exec(select(Post)).all()
    return{"All Posts":posts}

@app.get("/posts/{id}")
def get_post_by_id(id: int, db: SessionLocal):
    # cursor.execute(f"""SELECT * FROM posts WHERE id = {id};""")
    # post = cursor.fetchone()

    post = db.get(Post, id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} Not found")
    return {f"Post with id:{id}": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post_data : CreatePost, db: SessionLocal):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *;""",(post.title, post.content, post.published))
    # created_post = cursor.fetchone()
    # conn.commit()
    post = Post.model_validate(post_data)
    db.add(post)
    db.commit()
    db.refresh(post)
    return{"Post created successfully":post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: SessionLocal):
    # cursor.execute(f"""DELETE FROM posts WHERE id = {id} RETURNING *;""")
    # deleted_post = cursor.fetchone()
    post= db.get(Post, id)

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} could not be found")
    
    db.delete(post)
    db.commit()
    # conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post_data: models.UpdatePost, db: SessionLocal):
    # cursor.execute("""UPDATE posts SET title = %s, content= %s, published= %s WHERE id = %s RETURNING *;""",(post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    post = db.get(Post, id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} could not be found")
    
    update_data = post_data.model_dump()
    for key, value in update_data.items():
        setattr(post, key, value)

    db.add(post)
    db.commit()
    db.refresh(post)
    # conn.commit()
    return {"Post updated successfully": post}

@app.patch("/posts/{id}")
def patch_post(id: int, post_data: models.PatchPost, db: SessionLocal):
    # cursor.execute("""UPDATE posts SET title = %s, content= %s, published= %s WHERE id = %s RETURNING *;""",(post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    post = db.get(Post, id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} could not be found")
    
    update_data = post_data.model_dump()
    for key, value in update_data.items():
        if value != None:
            setattr(post, key, value)

    db.add(post)
    db.commit()
    db.refresh(post)
    # conn.commit()
    return {"Post updated successfully": post}