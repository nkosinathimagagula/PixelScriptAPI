from sqlalchemy.orm import Session

from database import crud
from security.password_hashing import verify_password

def authenticate_user(db: Session, email: str, password: str):
    db_user = crud.get_user(db=db, email=email)
    
    if db_user is None:
        return False
    
    if not verify_password(password, db_user.password):
        return False
    
    return db_user
