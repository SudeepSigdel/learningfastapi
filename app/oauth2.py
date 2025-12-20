from jose import jwt, JWTError
from datetime import datetime, timedelta
from . import models, database
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "login")

SECRET_KEY = "4f80f907b4a763a4b8d168e0359bce2a316d030c12c7cc3a4800f67bf1aa7336"
ALGORTIHM = "HS256"
EXPIRATION_TIME = 30

def create_token(payload: dict):
    expire =  datetime.utcnow() + timedelta(minutes= EXPIRATION_TIME)
    payload.update({"exp":expire})
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORTIHM)
    return token

def verify_token(token: str, credentials_error):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORTIHM])
        id = payload.get("user_id")
        if id == None:
            raise credentials_error

        user_id = models.TokenData(id=id)

    except JWTError:
        raise credentials_error
    
    return user_id

def get_current_user(db: database.SessionLocal, token = Depends(oauth2_scheme)):
    credentials_error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credentials Could not be verified", headers={"WWW_Authenticate":"Bearer"})

    payload = verify_token(token, credentials_error)

    user = db.get(models.User, payload.id)

    return user
