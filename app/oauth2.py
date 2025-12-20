from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "3876f6b377a80ed4135e4c68293097439a6f670ad3ed6d145f7544e8bcdea08c"
ALGORITHM = 'HS256'
EXPIRATION_TIME = 30

def create_token(data: dict):
    # {"user_id":10}

    to_encode = data.copy()
    # to_encode = {"user_id": 10}
    expire = datetime.now() + timedelta(minutes=EXPIRATION_TIME)
    # expire = now + expiration_time(30) ~ 520
    to_encode.update({"exp":expire})
    # {"user_id":10, "exp": 520}
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    # encoded_jwt = jwt.encode({"user_id":10, "exp": 520}, sdfhjghqhwiuduhqw9, 'HS256') ~ dnque98dh3893h.d8732tytd8732gd32.d23gd7326gd
    return encoded_jwt
