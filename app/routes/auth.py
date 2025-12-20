from fastapi import APIRouter, Depends, HTTPException, status
from ..database import SessionLocal
from sqlmodel import select
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, utils, oauth2

router = APIRouter(
    tags=['Authentication']
)

@router.post("/login", response_model=models.Token)
def login(db: SessionLocal, user_credentials: OAuth2PasswordRequestForm= Depends()):
    user = db.exec(select(models.User).where(models.User.email== user_credentials.username)).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    token = oauth2.create_token({"User_id": user.id})

    return {"access_token": token, "token_type": "bearer"}