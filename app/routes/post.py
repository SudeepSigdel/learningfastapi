from fastapi import APIRouter, HTTPException, Depends, status, Response
from ..database import SessionLocal
from .. import models, oauth2
from typing import List, Optional
from sqlmodel import select

router = APIRouter(
    prefix="/posts",
    tags=['post']
)

@router.get("/", response_model=List[models.PostResponse])
def get_all_user(db: SessionLocal, current_user= Depends(oauth2.get_current_user), limit: int= 10, skip: int= 0, search: Optional[str]=""):
    print(search)
    posts = db.exec(select(models.Post).where(models.Post.title.contains(search)).limit(limit).offset(skip)).all() # type: ignore
    return posts

@router.get("/{id}", response_model=models.PostResponse)
def get_user(id: int, db: SessionLocal, current_user = Depends(oauth2.get_current_user)):
    post = db.get(models.Post, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} Not Found")
    
    return post

@router.post("/", response_model=models.PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post_data: models.PostCreate, db: SessionLocal, current_user: models.User = Depends(oauth2.get_current_user)):
    post = models.Post(owner_id=current_user.id, **post_data.model_dump()) # type: ignore
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: SessionLocal, current_user = Depends(oauth2.get_current_user)):
    post = db.get(models.Post, id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} Not Found")
    
    if post.owner_id != current_user.id: # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Only Owner has this access")
    
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=models.PostResponse)
def post_update(id: int, post_data: models.PostUpdate, db: SessionLocal, current_user = Depends(oauth2.get_current_user)):
    post = db.get(models.Post, id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} Not Found")
    
    if post.owner_id != current_user.id: # type: ignore
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Only Owner has this access")
    
    post_dict = post_data.model_dump()
    for key, value in post_dict.items():
        setattr(post, key, value)

    return post