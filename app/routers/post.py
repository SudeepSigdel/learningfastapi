from fastapi import Response, status, HTTPException, APIRouter
from .. import models
from ..database import SessionLocal
from typing import List
from sqlmodel import select

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model= List[models.PostResponse])
def get_all_posts(db: SessionLocal):
    posts = db.exec(select(models.Post)).all()
    return posts

@router.get("/{id}", response_model= models.PostResponse)
def get_a_post(id: int, db: SessionLocal):
    post = db.get(models.Post, id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} Not found")
    
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=models.PostResponse)
def create_post(post_data : models.CreatePost, db: SessionLocal):
    post = models.Post.model_validate(post_data)

    db.add(post)
    db.commit()
    db.refresh(post)
    return {"Post Created Successfully": post}

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_a_post(id: int, db: SessionLocal):
    post = db.get(models.Post, id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} Not found")
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model= models.PostResponse)
def update_whole_post(post_data : models.UpdatePost, id: int, db: SessionLocal):
    post = db.get(models.Post, id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} Not found")
    
    updated_post = post_data.model_dump()

    for key, value in updated_post.items():
        setattr(post, key, value)

    db.add(post)
    db.commit()
    db.refresh(post)

    return{"Updated post": post}

@router.patch("/{id}", response_model=models.PostResponse)
def update_partial_post(post_data : models.PatchPost, id: int, db: SessionLocal):
    post = db.get(models.Post, id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} Not found")
    
    updated_post = post_data.model_dump()

    for key, value in updated_post.items():
        if value != None:
            setattr(post, key, value)

    db.add(post)
    db.commit()
    db.refresh(post)

    return{"Updated post": post}

