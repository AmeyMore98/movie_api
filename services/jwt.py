from datetime import timedelta, datetime 
from typing import Optional

from jose import JWTError, jwt

# Generated using: openssl rand -hex 32
SECRET_KEY = 'b0b8c74b7ef83e39fc9395050f68583fb8b6c643fa082d475518fe436ac6ddb5'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class JwtService:

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def decode_token(self, token):
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
