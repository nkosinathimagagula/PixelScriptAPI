from fastapi import FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.param_functions import Depends, Body, Header, File
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Annotated

from starlette.responses import JSONResponse

from PSM.PSTextract import extract_text
from database import models, crud
from database.database import SessionLocal, engine
from schemas.database_schema import UsersBase, Data
from schemas.response import Token, Detail
from security.token import oath2_scheme, ACCESS_TOKEN_EXPIRE_TIME, create_access_token, validate_token
from security.authenticate import authenticate_user
from utils.images import bytes_to_gray_image, file_type


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

## start of dependencies

def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()


def get_token_header(token: Annotated[str, Header()]):
    return token
        
## end of dependencies


## test connection !!!
@app.get("/")
def home():
    return JSONResponse(
        content={
            "status_code": status.HTTP_200_OK, 
            "message": "success"
        },
        status_code=200
    )


@app.post("/token", response_model=Token)
def generate_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = authenticate_user(db=db, email=form_data.username, password=form_data.password)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username/email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token_exp = timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
    
    access_token = create_access_token(
        details={"sub": user.email},
        expires=access_token_exp
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }
    


@app.post("/api/users/", response_model=Detail)
def create_user(user: Annotated[UsersBase, Body()], db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, email=user.email)
    
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Email '{db_user.email}' is already registered"
        )
    
    user_created = crud.create_user(db=db, user=user)
    
    return JSONResponse(
        content={"detail": user_created},
        status_code=status.HTTP_201_CREATED
    )


@app.post("/api/PST/extract/", response_model=Data)
async def extract(image: Annotated[bytes, File()], token:Annotated[str, Depends(get_token_header(oath2_scheme))], db: Session = Depends(get_db)):
    user = validate_token(db=db, token=token)
    
    gray_image = bytes_to_gray_image(image)
    
    PSM_result = extract_text(gray_image)
    
    data = {
        "text": PSM_result['text'],
        "headings": PSM_result['headings'],
        "file_type": file_type(image),
        "user_id": user.id
    }
    
    db_data = crud.add_data(db=db, data=data)
    
    return JSONResponse(
        content=db_data,
        status_code=status.HTTP_200_OK
    )
