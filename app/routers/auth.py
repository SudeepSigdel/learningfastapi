from fastapi import APIRouter, HTTPException, status, Depends
from .. import models, utils, database, oauth2
from sqlmodel import select
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])

@router.post("/login")
def login(db: database.SessionLocal, user_data: OAuth2PasswordRequestForm= Depends()):
    user = db.exec(select(models.User).where(models.User.email==user_data.username)).first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    if not utils.verify_password(user_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    token = oauth2.create_token(data={"user_id":user.id})

    return {"access_token":token, "token_type": "bearer"}