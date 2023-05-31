from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.param_functions import Body
from sqlalchemy.orm import Session
from typing import Annotated
from database import models, crud
from database.database import SessionLocal, engine
from schemas.database_schema import UsersBase, Users
from schemas.response import Detail

from starlette.responses import JSONResponse

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

## start of dependencies

def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        
## end of dependencies


## test connection !!!
@app.get("/")
def home():
    return JSONResponse(status_code=200, content={"status_code": status.HTTP_200_OK, "message": "success"})

####
@app.post("/api/users/", response_model=Detail)
def create_user(user: Annotated[UsersBase, Body()], db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user=user)
    
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
