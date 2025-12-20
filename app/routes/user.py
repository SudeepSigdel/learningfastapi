from fastapi import APIRouter, status, Depends, Response
from .. import models, utils, oauth2
from ..database import SessionLocal

router = APIRouter(
    prefix="/users",
    tags=["User"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=models.UserResponse)
def create_user(user_data: models.UserCreate, db: SessionLocal):
    user_data.password = utils.hash(user_data.password)
    user = models.User.model_validate(user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
        
@router.get("/{id}", response_model=models.UserResponse)
def get_user(id: int, db: SessionLocal, current_user: int = Depends(oauth2.get_current_user)):
    user = db.get(models.User, id)
    return user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: SessionLocal, current_user = Depends(oauth2.get_current_user)):
    user= db.get(models.User, id)
    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)