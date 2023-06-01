from sqlalchemy.orm import Session
from datetime import date

from schemas.database_schema import UsersBase, DataBase
from security.password_hashing import get_password_hash
from . import models
from utils.json import jsonify_data_record


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
    
    data_dict = jsonify_data_record(data)
    
    return data_dict


def get_data(db: Session, filter: dict):
    result = []
    db_response = []
    
    if filter['date'] is not None and filter['file_type'] is not None:
        db_response = db.query(models.Data).filter(models.Data.date <= filter['date'], models.Data.file_type == filter['file_type'], models.Data.user_id == filter['user_id']).all()
        
        for record in db_response:
            result.append(jsonify_data_record(record))
        
        return result
    elif filter['date'] is not None and filter['file_type'] is None:
        db_response = db.query(models.Data).filter(models.Data.date <= filter['date'], models.Data.user_id == filter['user_id']).all()
        
        for record in db_response:
            result.append(jsonify_data_record(record))
        
        return result
    elif filter['date'] is None and filter['file_type'] is not None:
        db_response = db.query(models.Data).filter(models.Data.file_type == filter['file_type'], models.Data.user_id == filter['user_id']).all()
        
        for record in db_response:
            result.append(jsonify_data_record(record))
        
        return result
    
    db_response = db.query(models.Data).filter(models.Data.user_id == filter['user_id']).all()
    
    for record in db_response:
        result.append(jsonify_data_record(record))
        
    return result
