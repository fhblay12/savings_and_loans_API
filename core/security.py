from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from repositories.admin_repo import get_admin_by_id
from fastapi.security import APIKeyHeader

api_key_scheme = APIKeyHeader(name="Authorization")


 

SECRET_KEY = "your_super_secret_key"  # keep this in .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict, expires_days: int = 7):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=expires_days)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/customer/login")  # token endpoint

def get_current_admin(token: str = Depends(api_key_scheme)):
    try:
        if not token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid auth header")
        token = token.split(" ")[1]

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "admin":
            raise HTTPException(status_code=403, detail="Admin access required")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(token: str = Depends(api_key_scheme)):
    try:
        if not token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid auth header")
        token = token.split(" ")[1]

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "customer":
            raise HTTPException(status_code=403, detail="Customer access required")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

oauth2_scheme_admin = OAuth2PasswordBearer(tokenUrl="/admin/login")

 