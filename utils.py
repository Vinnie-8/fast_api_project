from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, status
from database import settings  # lowercase 'settings' — the instance, not the class

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password[:72], hashed_password)


def hash_password(password):
    return pwd_context.hash(password[:72])


def create_access_token(data: dict) -> str:
    payload = data.copy()
    expiry = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    payload.update({"exp": expiry, "type": "access"})
    token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
    return token


def create_refresh_token(data: dict) -> str:
    payload = data.copy()
    expiry = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    payload.update({"exp": expiry, "type": "refresh"})
    token = jwt.encode(payload, settings.refresh_secret_key, algorithm=settings.algorithm)
    return token


def verify_access_token(token: str) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        if payload.get("type") != "access":
            raise credentials_exception
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception


def verify_refresh_token(token: str) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.refresh_secret_key, algorithms=[settings.algorithm])
        if payload.get("type") != "refresh":
            raise credentials_exception
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception