from sqlalchemy.orm import Session
from schemas.database_schema import UsersBase
from security.password_hashing import get_password_hash
from . import models


def get_user(db: Session, email: str):
    return db.query(models.Users).filter(models.Users.email == email).first()

def create_user(db: Session, user: UsersBase):
    hashed_passord = get_password_hash(user.password)
    db_user = models.Users(name=user.name, email=user.email, password=hashed_passord)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return "user created"
