from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="password", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connection with Database was Successful!")
        break
    except Exception as error:
        print("Connecting to Database failed!")
        print("Error: ", error)
        time.sleep(2)

class Post(BaseModel):
    title: str
    content: str
    published : bool = True


@app.get("/")
def index():
    return {"message": "Hello World!!"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"All posts": posts}

@app.get("/posts/{id}")
def get_post(id:int):
    cursor.execute(f"""SELECT * FROM posts WHERE id = {id}""")
    post = cursor.fetchone()
    if post == None:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} Not found!"))
    return {f"post with id:{id}": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",(post.title, post.content, post.published))
    post_dict = cursor.fetchone()
    conn.commit()
    return {"Post created Successfully":post_dict}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute(f"""DELETE FROM posts WHERE id = {id} RETURNING *""")
    post = cursor.fetchone()
    if post == None:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} Not found!"))
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()
    if updated_post == None:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} Not found!"))
    conn.commit()
    return {"post updated successfully":updated_post}