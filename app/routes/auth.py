from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, database, oauth2, utils
from sqlmodel import select

router = APIRouter(
    prefix="/login",
    tags=["Authenticate", "User"]
)

@router.post("/", response_model= models.Token)
def login(db: database.SessionLocal, user_credentials: OAuth2PasswordRequestForm= Depends()):
    user = db.exec(select(models.User).where(models.User.email == user_credentials.username)).first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    token = oauth2.create_token({"user_id": user.id})

    return {"access_token": token, "token_type": "bearer"}