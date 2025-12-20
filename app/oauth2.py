from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import models, database
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "0953c1e3077a31d655e26bdb3b281044bd2dfcb44b0400a377b3c8264d8aee29"
ALGORITHM = "HS256"
EXPIRATION_TIME = 30

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes= EXPIRATION_TIME)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get("User_id") # type: ignore

        if id is None:
            raise credentials_exception
        token_data = models.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data
    
def get_current_user(db: database.SessionLocal, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})

    user_data = verify_access_token(token, credentials_exception)

    user = db.get(models.User, user_data.id)

    return user