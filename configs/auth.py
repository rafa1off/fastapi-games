from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

from configs.exceptions import Forbidden
from pydantic import BaseModel

import os
from dotenv import load_dotenv

load_dotenv()

secret_key = str(os.getenv("SECRET_KEY"))
auth_algorithm = str(os.getenv("ALGORITHM"))
token_expire_minutes = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")


class TokenData(BaseModel):
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password) -> str:
    return pwd_context.hash(password)


def authenticate_user(user_data_password: str, user_hashed_password: str) -> bool:
    if not verify_password(user_data_password, user_hashed_password):
        return False
    else:
        return True


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=token_expire_minutes)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=auth_algorithm)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[auth_algorithm])
        username = payload.get("sub")
        if username is None:
            raise Forbidden

        token_data = TokenData(username=username)
    except JWTError:
        raise Forbidden

    return token_data
