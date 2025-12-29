from fastapi import APIRouter, HTTPException, status, Response, Depends
from .. import models, oauth2, database
from typing import Optional, List
from sqlmodel import select, func

router = APIRouter(
    prefix="/posts",
    tags=['Post']
)

@router.get("/", response_model=List[models.PostOut])
def get_posts(db: database.SessionLocal, limit: int = 10, skip: int = 0, search: Optional[str]=''):
    posts = db.exec(select(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, onclause=models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).where(models.Post.title.contains(search)).limit(limit).offset(skip)).all() #type: ignore
    return posts

@router.get("/{id}", response_model=models.PostOut)
def get_post_by_id(db: database.SessionLocal, id: int):
    post = db.exec(select(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, onclause=models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).where(models.Post.id == id)).first()#type:ignore
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} Not found")
    
    return post

@router.post("/", response_model= models.PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(db: database.SessionLocal, post_data: models.PostCreate, current_user: models.UserResponse =Depends(oauth2.get_current_user)):
    post = models.Post(owner_id=current_user.id, **post_data.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(db: database.SessionLocal, id: int, current_user: models.UserResponse= Depends(oauth2.get_current_user)):
    post = db.get(models.Post, id)

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} Not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the post creator")
    
    db.delete(post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@router.put("/{id}", response_model=models.PostResponse)
def Update_post(db: database.SessionLocal, id:int, post_data: models.PostUpdate, current_user: models.UserResponse=Depends(oauth2.get_current_user)):
    post = db.get(models.Post, id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} Not Found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="You are not the post creator")
    
    post_dict = post_data.model_dump()
    for key, value in post_dict.items():
        setattr(post, key, value)

    db.add(post)
    db.commit()
    db.refresh(post)

    return post