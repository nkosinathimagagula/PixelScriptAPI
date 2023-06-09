from sqlalchemy.orm import Session

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
    
    from_date = filter['from_date']
    to_date = filter['to_date']
    file_type = filter['file_type']
    user_id = filter['user_id']
    
    if from_date is not None and to_date is not None and file_type is not None:
        db_response = db.query(models.Data).filter(models.Data.date >= from_date, models.Data.date <= to_date, models.Data.file_type == file_type, models.Data.user_id == user_id).all()
        
        for record in db_response:
            result.append(jsonify_data_record(record))
        
        return result
    elif from_date is not None and to_date is not None and file_type is None:
        db_response = db.query(models.Data).filter(models.Data.date >= from_date, models.Data.date <= to_date, models.Data.user_id == user_id).all()
        
        for record in db_response:
            result.append(jsonify_data_record(record))
        
        return result
    elif from_date is not None and to_date is None and file_type is not None:
        db_response = db.query(models.Data).filter(models.Data.date >= from_date, models.Data.file_type == file_type, models.Data.user_id == user_id).all()
        
        for record in db_response:
            result.append(jsonify_data_record(record))
        
        return result
    elif from_date is None and to_date is not None and file_type is not None:
        db_response = db.query(models.Data).filter(models.Data.date <= to_date, models.Data.file_type == file_type, models.Data.user_id == user_id).all()
        
        for record in db_response:
            result.append(jsonify_data_record(record))
        
        return result
    elif from_date is None and to_date is None and file_type is not None:
        db_response = db.query(models.Data).filter(models.Data.file_type == file_type, models.Data.user_id == user_id).all()
        
        for record in db_response:
            result.append(jsonify_data_record(record))
        
        return result
    elif from_date is not None and to_date is None and file_type is None:
        db_response = db.query(models.Data).filter(models.Data.date >= from_date, models.Data.user_id == user_id).all()
        
        for record in db_response:
            result.append(jsonify_data_record(record))
    
        return result
    elif from_date is None and to_date is not None and file_type is None:
        db_response = db.query(models.Data).filter(models.Data.date <= to_date, models.Data.user_id == user_id).all()
        
        for record in db_response:
            result.append(jsonify_data_record(record))
    
        return result
    
    
    db_response = db.query(models.Data).filter(models.Data.user_id == filter['user_id']).all()
    
    for record in db_response:
        result.append(jsonify_data_record(record))
        
    return result
