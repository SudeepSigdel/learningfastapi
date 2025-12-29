from .. import models, database, oauth2
from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel import select

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote_post(vote: models.VoteInput, db: database.SessionLocal, current_user= Depends(oauth2.get_current_user)):
    post = db.get(models.Post, vote.post_id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{vote.post_id} not found")
    
    found_vote = db.exec(select(models.Vote).where(vote.post_id == models.Vote.post_id, models.Vote.user_id == current_user.id)).first()

    if vote.direction == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User:{current_user.id} has already voted on the post:{vote.post_id}")
        
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)

        db.add(new_vote)
        db.commit()
        return {"message":"Vote added successfully!"}
    
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User:{current_user.id} has not voted on the post:{vote.post_id}")
        
        db.delete(found_vote)
        db.commit()

        return{"message":"Vote removed successfully!"}
