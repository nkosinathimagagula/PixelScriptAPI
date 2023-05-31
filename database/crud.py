from sqlalchemy.orm import Session
from datetime import date

from schemas.database_schema import UsersBase, DataBase
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


def add_data(db: Session, data: DataBase):
    data = models.Data(text=data['text'], headings=data['headings'], file_type=data['file_type'], user_id=data['user_id'])
    
    db.add(data)
    db.commit()
    db.refresh(data)
    
    data_dict = {
        "id": data.id,
        "text": data.text,
        "headings": data.headings,
        "file_type": data.file_type,
        "date": date.strftime(data.date, "%Y-%m-%d"),
        "user_id": data.user_id
    }
    
    return data_dict
