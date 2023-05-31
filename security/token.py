from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from typing import Annotated

from database import crud


SECRET_KEY = "cb234b31a275744ab80d65190bdb2c573167c371c89ddf47c5841273adc48a7a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_TIME = 60

oath2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(details: dict, expires: timedelta | None = None):
    to_encode = details
    
    if expires:
        expires = datetime.utcnow() + expires
    else:
        expires = datetime.utcnow + timedelta(minutes=30)
    
    to_encode.update({"exp": expires})
    
    encoded_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def get_current_user(db: Session, token: Annotated[str, Depends(oath2_scheme)]):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
        
        email = payload.get("sub")
        
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credintials",
                headers={"WWW-Authenticate": "Bearer"}
            )
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credintials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    db_user = crud.get_user(db=db, email=email)
    
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credintials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return db_user


def validate_token(db: Session, token: str):
    user = get_current_user(db=db, token=token)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin token",
            headers={"WWW-Authenticate": "Bearer"}
        )
