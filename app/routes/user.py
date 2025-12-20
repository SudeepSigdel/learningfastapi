from .. import models, database, utils, oauth2
from fastapi import APIRouter, status, HTTPException, Depends

router = APIRouter(
    prefix="/users",
    tags=['User']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=models.UserResponse)
def create_user(db: database.SessionLocal, user_data: models.UserCreate):
    user_data.password = utils.hash(user_data.password)
    user = models.User.model_validate(user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/{id}", response_model=models.UserResponse)
def get_user(id: int, db: database.SessionLocal, current_user= Depends(oauth2.get_current_user)):
    user = db.get(models.User, id)
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id:{id} Not found")
    return user