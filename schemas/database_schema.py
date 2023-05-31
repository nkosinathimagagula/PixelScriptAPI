from pydantic import BaseModel
from datetime import date

class UsersBase(BaseModel):
    name: str
    email: str
    password: str

class Users(UsersBase):
    id: int
    
    class Config:
        orm_mode = True

class DataBase(BaseModel):
    text: str
    file_type: str
    
    user_id: int
    
class Data(DataBase):
    id: str
    date: date
